import subprocess

from flask import Flask, Response, jsonify
from graph_word import plot_word, word_metadata

app = Flask(__name__, static_url_path='/static', static_folder='public')

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
    app.run(host="0.0.0.0")
