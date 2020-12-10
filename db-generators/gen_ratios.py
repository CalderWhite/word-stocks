"""
Generates the ratios for the past n periods.
This script can be configured to generate ratios for different time period
and offsets.

NOTE: Q1 is represented as 0 in terms of period "index"
"""
from multiprocessing import Pool
from datetime import datetime
import calendar

import psycopg2
from tqdm import tqdm

# 1 : yearly
# 4 : periodly
# 12 : monthly
frequency = 12


def generate_ratios(period):
    conn_string = "dbname='investment_data' user='calder' host='localhost'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    begin_closes = {}

    # figuring out the dates
    year = period//frequency
    month = (period%frequency)*(12//frequency) + 1
    firstday = 1
    _, lastday = calendar.monthrange(year, month+(12//frequency - 1))

    first_timestamp = datetime(year, month, firstday).timestamp()
    last_timestamp = datetime(year, month+(12//frequency - 1), lastday).timestamp()

    # get the initial closes of the period
    cursor.execute(f"""
        SELECT DISTINCT ON (symbol) symbol, close FROM stocks
        WHERE timestamp BETWEEN {first_timestamp} AND {last_timestamp}
        ORDER BY symbol, timestamp ASC;
    """)
    for symbol, close in cursor.fetchall():
        begin_closes[symbol] = close

    # get the final closes of the period and calculate the ratio of final/initial
    cursor.execute(f"""
        SELECT DISTINCT ON (symbol) symbol, close FROM stocks
        WHERE timestamp BETWEEN {first_timestamp} AND {last_timestamp}
        ORDER BY symbol, timestamp DESC;
    """)
    rows = []
    for symbol, close in cursor.fetchall():
        if close is None or begin_closes[symbol] is None:
            continue
        rows.append((symbol, period, close/begin_closes[symbol]))

    cursor.executemany("INSERT INTO periodly_ratios(symbol, period, ratio)\
                       VALUES(%s, %s, %s)", rows)
    conn.commit()


def main():
    # postgresql will parallelize on its own due to the BETWEEN condition
    # however, for each SELECT query it only spawns 2 other threads for a total
    # of 3, so adding in a multiprocessing pool with 2 workers does increase
    # performance a little bit
    today = datetime.today()
    current_period = today.year*frequency + today.month//(12//frequency)
    p = Pool(2)
    for i in tqdm(p.imap_unordered(generate_ratios,
                                 range(current_period,
                                       current_period-20*frequency, -1)), total=20*frequency):
        pass


if __name__ == '__main__':
    main()
