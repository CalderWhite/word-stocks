import sys
import io

import psycopg2

# this allows us to not have an X server running
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.backends.backend_agg import FigureCanvasAgg

from tabulate import tabulate


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

    x = []
    y = []
    y2 = []
    for year, wp, mr in cursor:
        x.append(year)
        y.append(wp)
        y2.append(mr)

    #r = [(i/y[0] - 1)*100 for i in y]
    #r2 = [i/y2[0] for i in y2]
    # the second are already ratios, so if we want to see the relationship
    # of the _close_ to the first close, we just multiply the ratios by eachother
    r2 = [1]
    current_ratio = 1
    for i in y2[1:]:
        current_ratio *= i

        # we dont want negative values in a chart.
        if chart:
            r2.append(current_ratio*100)
        else:
            r2.append((current_ratio - 1)*100)

    return x, r2


def plot_word(word, output_format='svg'):
    
    x, r2 = get_word_data(word)

    plt.style.use('gadfly_dark')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(decimals=2))

    fig = Figure(figsize=(10, 5))
    axis = fig.add_subplot(1, 1, 1)

    #axis.plot(x, r, x, r2)
    #axis.legend(['Win Percent', 'Close'])
    axis.plot(x, r2)
    axis.legend(['Close'])
    axis.set_xlabel('Year')
    axis.set_ylabel(f'% Change since {int(x[0])}')
    fig.suptitle(f'Performance of stocks containing "{word}" v Time')

    #plt.savefig("word_graph.svg", edgecolor="black")
    output = io.BytesIO()
    if output_format == 'svg':
        FigureCanvasSVG(fig).print_svg(output)
    elif output_format == 'png':
        FigureCanvasAgg(fig).print_png(output)

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

    table = [("Match Count:", str(symbol_count)), ("Exchanges:", "NYSE, Nasdaq, TSX")]
    html = tabulate(table, tablefmt="html")

    return html


if __name__ == '__main__':
    plot_svg = plot_word(sys.argv[1])
    open("out.svg", 'wb').write(plot_svg.getvalue())
