"""
This script should only be run once to populate the words table.
"""
from multiprocessing import Pool

from tqdm import tqdm
import psycopg2

import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


words = {}


def get_terms(symbol):
    conn_string = "dbname='investment_data' user='calder' host='localhost'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cursor.execute(f"SELECT description FROM stock_metadata\
                        WHERE symbol='{symbol}'")
    fetched = cursor.fetchone()
    if fetched is None:
        return

    desc = fetched[0]
    if desc is None:
        return

    desc = desc.lower()

    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(desc)
    filtered = [word for word in tokens if word not in stopwords.words()]
    filtered = set(filtered)

    rows = [(symbol, i) for i in filtered]

    cursor.executemany("INSERT INTO words(symbol, word) VALUES (%s, %s)", rows)
    conn.commit()


conn_string = "dbname='investment_data' user='calder' host='localhost'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

cursor.execute("SELECT symbol FROM symbols;")
symbols = [i[0] for i in cursor.fetchall()]

p = Pool()
for _ in tqdm(p.imap_unordered(get_terms, symbols), total=len(symbols)):
    pass
p.close()
p.join()
