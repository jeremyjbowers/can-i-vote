#!/usr/bin/env python
import os

from flask import Flask
from flask import render_template, request
from tropo import Tropo
import json

app = Flask(__name__)


@app.route('/helloworld.json', methods=['GET'])
def hello():
    tropo = Tropo()
    tropo.say("Hello, World")
    return tropo.RenderJson()


@app.route('/state0.json', methods=['GET'])
def state_0():
    tropo = Tropo()
    tropo.ask(choices="[ANY]", say="Ahoy-hoy! Tell us, what state do you live in?", timeout=60)
    return tropo.RenderJson()


@app.route('/', methods=['GET'])
def homepage():
    return """
<html>
    <head>
    <style type="text/css">
        * {
            margin:0;
            padding:0;
            font-size:64px;
        }
        body {
            color:#fdf6e3;
            background-color:#002b36;
            font-size:64px;
            font-family:Helvetica,'Helvetica',sans-serif;
            margin:20px auto;
            min-width:320px;
            max-width:1024px;
            display:block;
            text-align:center;
        }
        a {
            font-weight:bold;
            color:#cb4b16;
            text-decoration:none;
        }
        code {
            color:#d33682;
            font-weight:bold;
        }
    </style>
    </head>
    <body>
        <p>Text <code>vote</code> to <a href="sms:+12027385185">(202) 738-5185</a>.</p>
    </body>
</html>
"""

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
