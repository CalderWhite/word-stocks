import subprocess

from flask import Flask, Response, jsonify, redirect, request
from flask_talisman import Talisman

from graph_word import plot_word, word_metadata

PROD = True
SSL_CERT_PATH = "/etc/letsencrypt/live/word-stocks.calderwhite.me/fullchain.pem"
SSL_PRIVATE_KEY_PATH = "/etc/letsencrypt/live/word-stocks.calderwhite.me/privkey.pem"

app = Flask(__name__, static_url_path='/static', static_folder='public')
# currently using some unsafe practices with the CDNS. Will deal with later.
#Talisman(app)


@app.route('/graph_word/<word>')
def graph_word_endpoint(word):
    graph_svg = plot_word(word)
    return Response(graph_svg.getvalue(), mimetype="image/svg+xml")


@app.route('/word_metadata/<word>')
def word_metadata_endpoint(word):
    return jsonify(word_metadata(word))


@app.route('/')
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    if not PROD:
        app.run(host="0.0.0.0")
    else:
        app.run(host="0.0.0.0", port=443, ssl_context=(SSL_CERT_PATH, SSL_PRIVATE_KEY_PATH))
