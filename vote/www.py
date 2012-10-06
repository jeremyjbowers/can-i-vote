#!/usr/bin/env python

from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def jason_sucks():
    """
    Tell the world about Jason.
    """

    return """
        <html>
            <body>
                <h1>JASON FUCKING SUCKS</h1>
            </body>
        </html>
    """