#!/usr/bin/env python

from datetime import datetime
import json
from sets import Set

from flask import Flask
from flask import render_template, request
import pytz

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