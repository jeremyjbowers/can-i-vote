#!/usr/bin/env python
import os

from flask import Flask
from flask import render_template, request
from tropo import Tropo
import json
from mongolier import Connection

app = Flask(__name__)

@app.route('/helloworld.json', methods=['GET', 'POST'])
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
        context = {}
        return render_template('index.html', **context)

    if request.method == "POST":
        data = get_request(request)

        state = None
        user_id = data['session']['from']['id']
        sms_text = data['session']['initialText']

        state = determine_state(data)

        if state == 0:
            tropo = Tropo()
            tropo.say("Hello, %s! What state do you live in?" % user_id)
            connection.api.find_and_modify(
                query={"user_id":user_id},
                update={"user_id":user_id,"state":1,"geographic_state":None},
                upsert=True)
            return tropo.RenderJson()

        if state == 1:
            connection.api.find_and_modify(
                query={"user_id":user_id},
                update={"user_id":user_id,"state":2,"geographic_state":sms_text},
                upsert=True)
            tropo = Tropo()
            tropo.say("Hi, %s! Are you registered to vote in %s?" % (user_id, sms_text))
            return tropo.RenderJson()

        if state == 2:
            tropo = Tropo()
            
            if "y" in sms_text.lower():
                # This is where we check if you have a driver license.
                connection.api.find_and_modify(
                    query={"user_id":user_id},
                    update={"user_id":user_id,"state":0, "geographic_state":None},
                    upsert=True)
                tropo.say("Congratulations, %s! You can vote! Call (555) 555-5555 for more information." % user_id)
            
            elif "n" in sms_text.lower():
                # This is where we check if the voter registration has passed.
                connection.api.find_and_modify(
                    query={"user_id":user_id},
                    update={"user_id":user_id,"state":0, "geographic_state":None},
                    upsert=True)
                tropo.say("Your voter registration date has passed, %s. We has a sad." % user_id)
            
            else:
                # We didn't get a yes or a no from the user.
                tropo.say("We didn't understand your response, %s. Please respond with yes or no." % user_id)
            
            return tropo.RenderJson()

        if state == None:
            tropo = Tropo()
            tropo.say("Sorry, we lost you there. What state do you live in?")
            # Set the state to 0 for this user.
            return tropo.RenderJson()

@app.route('/', methods=['GET'])
def homepage():
    context = {}
    return render_template('index.html', **context)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
