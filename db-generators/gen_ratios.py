"""
Generates the ratios for the past n quarters.
This script can be configured to generate ratios for different time period
and offsets.

NOTE: Q1 is represented as 0 in terms of quarter "index"
"""
from multiprocessing import Pool
from datetime import datetime
import calendar

import psycopg2
from tqdm import tqdm


def generate_ratios(quarter):
    conn_string = "dbname='investment_data' user='calder' host='localhost'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    begin_closes = {}

    # figuring out the dates
    year = quarter//4
    month = (quarter%4)*3 + 1
    firstday = 1
    _, lastday = calendar.monthrange(year, month+2)

    first_timestamp = datetime(year, month, firstday).timestamp()
    last_timestamp = datetime(year, month+2, lastday).timestamp()

    # get the initial closes of the quarter
    cursor.execute(f"""
        SELECT DISTINCT ON (symbol) symbol, close FROM stocks
        WHERE timestamp BETWEEN {first_timestamp} AND {last_timestamp}
        ORDER BY symbol, timestamp ASC;
    """)
    for symbol, close in cursor.fetchall():
        begin_closes[symbol] = close

    # get the final closes of the quarter and calculate the ratio of final/initial
    cursor.execute(f"""
        SELECT DISTINCT ON (symbol) symbol, close FROM stocks
        WHERE timestamp BETWEEN {first_timestamp} AND {last_timestamp}
        ORDER BY symbol, timestamp DESC;
    """)
    rows = []
    for symbol, close in cursor.fetchall():
        if close is None or begin_closes[symbol] is None:
            continue
        rows.append((symbol, quarter, close/begin_closes[symbol]))

    cursor.executemany("INSERT INTO quarterly_ratios(symbol, quarter, ratio)\
                       VALUES(%s, %s, %s)", rows)
    conn.commit()


def main():
    # postgresql will parallelize on its own due to the BETWEEN condition
    # however, for each SELECT query it only spawns 2 other threads for a total
    # of 3, so adding in a multiprocessing pool with 2 workers does increase
    # performance a little bit
    today = datetime.today()
    current_quarter = today.year*4 + today.month//3
    p = Pool(2)
    for i in tqdm(p.imap_unordered(generate_ratios,
                                 range(current_quarter,
                                       current_quarter-20*4, -1)), total=20*4):
        pass


if __name__ == '__main__':
    main()
