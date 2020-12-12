import sys
import io
from multiprocessing import Pool

import psycopg2
from tqdm import tqdm



def get_word_data(word, chart=False):
    conn_string = "dbname='investment_data' user='calder' host='localhost'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            CAST(period AS float)/12,
            win_percent,
            median_ratio
        FROM word_scores
        WHERE
            word='{word}' ORDER BY period ASC
    """)

    cursor.fetchall()


def word_metadata(word):
    conn_string = "dbname='investment_data' user='calder' host='localhost'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    # get the number of symbols 

    cursor.execute(f"""
        SELECT
            COUNT(*)
        FROM words
        WHERE
            word='{word}';
    """)

    symbol_count = cursor.fetchone()[0]


def main():
    conn_string = "dbname='investment_data' user='calder' host='localhost'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT word FROM words")

    words = [i[0] for i in cursor.fetchall()]

    # number of threads depends on the machine this is running on
    # I have found 4 crashes my 16 thread SSD box
    p = Pool(1)
    for i in tqdm(p.imap_unordered(get_word_data, words), total=len(words)):
        pass
    

if __name__ == '__main__':
    main()
