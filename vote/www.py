#!/usr/bin/env python

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
    <body style="color:#fdf6e3;background-color:#002b36;font-size:64px;font-family:Helvetica,'Helvetica',sans-serif;margin:20px auto;width:1024px;display:block;text-align:center;">
        <h1 style="font-size:128px;">Can I vote?</h1>
        <p>Text <code style="color:#d33682;font-weight:bold;">vote</code> to 2274.</p>
    </body>
</html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)