"""
The goal of this script is to find up and coming words.

Outputs the words at findal_quarter based on the max amount of quarters its
win_percent has been increasing and its current median_ratio, in that order
of priority.
"""
from tabulate import tabulate
import psycopg2

conn_string = "dbname='investment_data' user='calder'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()


def get_win_percents(quarters):
    quarter_wins = {}
    for quarter in quarters:
        cursor.execute(f"""
            SELECT word, win_percent FROM word_scores
            WHERE
                quarter = {quarter};
        """)

        for word, win_percent in cursor.fetchall():
            if word not in quarter_wins:
                quarter_wins[word] = []

            quarter_wins[word].append(win_percent)
    return quarter_wins


def get_growing(final_quarter, quarters_in_past):
    quarters = list(range(final_quarter - quarters_in_past, final_quarter + 1))
    quarter_wins = get_win_percents(quarters)

    cursor.execute(f"""
        SELECT * FROM word_scores
        WHERE
            quarter = {final_quarter} AND total > 1
    """)
    out = []
    none_count = 0
    for row in cursor:
        word = row[0]
        if word not in quarter_wins:
            none_count += 1
            continue
        history = quarter_wins[word]
        ratios = [
            1 if history[i-1] == 0 else history[i]/history[i-1]
            for i in range(1, len(history)-1)
        ]

        if len(ratios) == 0:
            continue

        """
        max_up = 0
        count = 0
        counting = True
        for i in ratios:
            if counting:
                if i > 1.0:
                    count += 1
                else:
                    counting = False
            else:
                if i > 1.0:
                    counting = True
                    count = 1

            if count > max_up:
                max_up = count
        """
        max_up = 0
        for i in ratios:
            if i > 1.0:
                max_up += 1

        #max_up = max_up if max_up > count else count

        out += [[max_up] + list(row)]

    out.sort(key=lambda k: (k[0], k[-2]), reverse=True)
    return out


def main():
    current = get_growing(2019*4, 5*4)
    prev = get_growing(2019*4-1, 5*4)
    c_words = [row[1] for row in prev]

    diffs = []

    for i in range(len(current)):
        word = current[i][1]
        if word not in c_words:
            text = "NULL"
        else:
            old_rank = c_words.index(word)
            diff = old_rank - i
            diffs.append(diff)

            sign = "+" if diff > 0 else ""
            text = sign + str(diff) if diff != 0 else "--"
            current[i].insert(0, text)

    current = current[:20]
    print(tabulate(current, headers=["mcu", "word", "quarter", "total",
                                     "win_percent", "mean_ratio",
                                     "median_ratio"]))
    #print(good/total, "(", good, "/", total, ")")


if __name__ == '__main__':
    main()
