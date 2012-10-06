#!/usr/bin/env python
import os

from flask import Flask
from flask import render_template, request
from tropo import Tropo
import json
from mongolier import Connection

app = Flask(__name__)

<<<<<<< HEAD
template = """
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

@app.route('/helloworld.json', methods=['GET'])
def hello():
    tropo = Tropo()
    tropo.say("Hello, World")
    return tropo.RenderJson()

@app.route('/vote.json', methods=['GET', 'POST'])
def vote():

    # Set up the mongo connection.
    connection = Connection(db="canivote", collection="users")

    def get_request(request):
        """
        Get the request and turn it into a dictionary.
        """
        return dict(json.loads(request.data))

    def determine_state(data):
        """
        Get this user and determine their state.
        """
        # Find this user.
        state = connection.api.find_one(query={"user_id":user_id})
        
        # If they have a state, return it. Otherwise, return nothing.
        if state:
            return state['state']
        else:
            return 0

    if request.method == "GET":
        return template

    if request.method == "POST":
        data = get_request(request)

        state = None
        user_id = data['session']['from']['id']
        sms_text = data['session']['initialText']

        state = determine_state(data)

        if state == 0:
            tropo = Tropo()
            tropo.say("Hello! What state do you live in?")
            connection.api.find_and_modify(
                query={"user_id":user_id},
                update={"user_id":user_id,"state":1, "geographic_state":None},
                upsert=True)
            return tropo.RenderJson()

        if state == 1:

            connection.api.find_and_modify(
                query={"user_id":user_id},
                update={"user_id":user_id,"state":2, "geographic_state":sms_text},
                upsert=True)
            tropo = Tropo()
            tropo.say("Are you registered to vote in %s?" % sms_text)
            return tropo.RenderJson()

        if state == 2:
            tropo = Tropo()

            if "y" in sms_text.lower():
                tropo.say("We didn't understand your response. Please respond with yes or no." % geographic_state)

            elif "n" in sms_text.lower():
                connection.api.find_and_modify(
                    query={"user_id":user_id},
                    update={"user_id":user_id,"state":2, "geographic_state":geographic_state},
                    upsert=True)
            else:
                tropo.say("We didn't understand your response. Please respond with yes or no." % geographic_state)

            return tropo.RenderJson()

        if state == None:
            tropo = Tropo()
            tropo.say("Sorry, we lost you there. What state do you live in?")
            # Set the state to 0 for this user.
            return tropo.RenderJson()

@app.route('/', methods=['GET'])
def homepage():
    return template

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
