#!/usr/bin/env python

from flask import Flask
from flask import render_template, request
from tropo import Tropo

app = Flask(__name__)

@app.route('/helloworld.json', methods=['GET'])
def hello():
    tropo = Tropo()
    tropo.say("Hello, World")
    return tropo.RenderJson()

@app.route('/', methods=['GET'])
def homepage():
    return "<html><body>Can I vote? Text <code>can i vote</code> to 2274</body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)