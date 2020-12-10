from datetime import datetime
from multiprocessing import Pool

import psycopg2
from tqdm import tqdm

frequency = 12


def get_word_totals(cursor, period):
    cursor.execute(f"""
        SELECT
            word,
            COUNT(*) FILTER (
                WHERE symbol IN (
                    SELECT DISTINCT symbol
                    FROM periodly_ratios WHERE period = {period}
                )
            ) as word_count
        FROM words
        GROUP BY word
        ORDER BY word_count DESC;
    """)

    return cursor.fetchall()


def get_winning_words(cursor, period):
    cursor.execute(f"""
        SELECT word, COUNT(*) as word_count FROM words
        WHERE symbol IN (
            SELECT symbol FROM periodly_ratios
            WHERE
                period = {period} AND
                ratio >= 1.0
        )
        GROUP BY word
        ORDER BY word_count DESC;
    """)

    win_count_map = {}
    for word, win_count in cursor:
        win_count_map[word] = win_count

    return win_count_map


def get_ratio_map(cursor, period):
    cursor.execute(f"""
        SELECT symbol, ratio FROM periodly_ratios WHERE period = {period}
    """)
    ratio_map = {}
    for symbol, ratio in cursor:
        ratio_map[symbol] = ratio

    return ratio_map


def generate_period_scores(period):
    conn_string = "dbname='investment_data' user='calder' host='localhost'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    #print("Calculating", period, "...")
    word_totals = get_word_totals(cursor, period)
    win_count_map = get_winning_words(cursor, period)
    ratio_map = get_ratio_map(cursor, period)

    win_percent_map = {}
    for word, total in word_totals:
        if word not in win_count_map:
            win_percent_map[word] = (total, 0)
        else:
            win_percent_map[word] = (total, win_count_map[word]/total)

    # group the symbols by word and calculate all the scores
    cursor.execute("""
        WITH good_words AS (
            SELECT word FROM words GROUP BY word
        )
        SELECT word, array_agg(symbol) FROM words
        WHERE
            word IN (SELECT * FROM good_words)
        GROUP BY word
    """)
    out_rows = []
    for word, symbol_list in cursor:
        ratios = []
        for symbol in symbol_list:
            if symbol in ratio_map:
                ratios.append(ratio_map[symbol])

        if len(ratios) == 0:
            continue

        mean = sum(ratios)/len(ratios)
        # calculate the median
        ratios.sort()
        rlen = len(ratios)
        if len(ratios) % 2 == 0:
            median = ratios[rlen//2 - 1] + ratios[rlen//2]
            median /= 2
        else:
            median = ratios[rlen//2]

        total, win_percent = win_percent_map[word]
        out_rows.append((word, period, total, win_percent, mean, median))

    #print("Inserting", period, "...")
    headers = ['word', 'period', 'total', 'win_percent', 'mean_ratio',
               'median_ratio']
    header = ",".join(headers)
    template = ",".join(["%s"]*len(headers))
    cursor.executemany(f"INSERT INTO word_scores({header}) VALUES({template})",
                       out_rows)
    conn.commit()


def main():
    today = datetime.today()
    current_period = today.year*frequency + today.month//(12//frequency)
    # don't over parallelize. work out how many workers is right for your setup.
    p = Pool(4)
    for i in tqdm(p.imap_unordered(generate_period_scores,
                                 range(current_period,
                                       current_period-20*frequency, -1)), total=20*frequency):
        pass


if __name__ == '__main__':
    main()
