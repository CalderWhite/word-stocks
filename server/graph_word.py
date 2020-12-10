import sys
import io

import psycopg2
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_svg import FigureCanvasSVG

from tabulate import tabulate


def plot_word(word):
    conn_string = "dbname='investment_data' user='calder' host='localhost'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            CAST(quarter AS float)/4,
            win_percent,
            median_ratio
        FROM word_scores
        WHERE
            word='{word}' ORDER BY quarter ASC
    """)

    x = []
    y = []
    y2 = []
    for year, wp, mr in cursor:
        x.append(year)
        y.append(wp)
        y2.append(mr)

    r = [(i/y[0] - 1)*100 for i in y]
    #r2 = [i/y2[0] for i in y2]
    # the second are already ratios, so if we want to see the relationship
    # of the _close_ to the first close, we just multiply the ratios by eachother
    r2 = [1]
    current_ratio = 1
    for i in y2[1:]:
        current_ratio *= i
        r2.append((current_ratio - 1)*100)

    plt.style.use('gadfly_dark')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(decimals=2))

    fig = Figure(figsize=(10, 5))
    axis = fig.add_subplot(1, 1, 1)

    axis.plot(x, r, x, r2)
    axis.legend(['Win Percent', 'Close'])
    axis.set_xlabel('Year')
    axis.set_ylabel(f'% Change since {x[0]}')
    fig.suptitle(f'Performance of stocks containing "{word}" v Time')

    #plt.savefig("word_graph.svg", edgecolor="black")
    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)

    return output

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
    print(symbol_count)

    table = [("Match Count:", str(symbol_count)), ("Exchanges:", "NYSE, Nasdaq, TSX")]
    html = tabulate(table, tablefmt="html")

    return html


if __name__ == '__main__':
    print(word_metadata(sys.argv[1]))
    #plot_svg = plot_word(sys.argv[1])
    #open("out.svg", 'wb').write(plot_svg.getvalue())
