import subprocess
from datetime import datetime

from flask import Flask, Response, jsonify, redirect, request

from graph_word import plot_word, get_word_data, word_metadata

PROD = False
SSL_CERT_PATH = "/etc/letsencrypt/live/word-stocks.calderwhite.me/fullchain.pem"
SSL_PRIVATE_KEY_PATH = "/etc/letsencrypt/live/word-stocks.calderwhite.me/privkey.pem"

app = Flask(__name__, static_url_path='/static', static_folder='public')
# currently using some unsafe practices with the CDNS. Will deal with later.


@app.route('/api/words/<word>/graph')
def graph_word_endpoint(word):
    graph_svg = plot_word(word)
    return Response(graph_svg.getvalue(), mimetype="image/svg+xml")


@app.route('/api/words/<word>/historical_data')
def get_word_data_endpoint(word):
    x, y = get_word_data(word, chart=True)

    # format the data for tradingview
    data_points = []

    # make it as though we start at 100 (perhaps $100, for example),
    # and see where we end up based on the ratios
    for i in range(len(x)):
        # convert the year (which includes its decimals) to a timestamp
        timestamp = (x[i] - 1970)*(365*24*60*60)
        time_str = str(datetime.fromtimestamp(timestamp)).split(" ")[0]

        data_points.append({"time": time_str, "value": y[i]})

    return jsonify({"chart": data_points})


@app.route('/api/words/<word>/metadata')
def word_metadata_endpoint(word):
    return jsonify(word_metadata(word))


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/')
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    if not PROD:
        app.run(host="0.0.0.0")
    else:
        app.run(host="0.0.0.0", port=443, ssl_context=(SSL_CERT_PATH, SSL_PRIVATE_KEY_PATH))
