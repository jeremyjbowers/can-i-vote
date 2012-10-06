#!/usr/bin/env python
import os

from flask import Flask
from flask import render_template, request
from tropo import Tropo
import json
from mongolier import Connection

app = Flask(__name__)

class Voter(object):

    # Set up the mongo connection.
    connection = Connection(db="canivote", collection="users")
    user_id = None
    sms_text = None
    state = None
    data = None

    def run(self, request):
        if request.method == "GET":
            context = {}
            return render_template('index.html', **context)

        if request.method == "POST":
            self.data = self.get_request(request)
            self.set_basic_params()
            self.state = self.determine_state()

            if self.state == 0:
                self.connection.api.find_and_modify(
                    query={"user_id":self.user_id},
                    update={"user_id":self.user_id,"state":1,"geographic_state":None},
                    upsert=True)
                tropo = Tropo()
                tropo.say("Hello, %s! What state do you live in?" % self.user_id)
                return tropo.RenderJson()

            if self.state == 1:
                self.connection.api.find_and_modify(
                    query={"user_id":self.user_id},
                    update={"user_id":self.user_id,"state":2,"geographic_state":self.sms_text},
                    upsert=True)
                tropo = Tropo()
                tropo.say("Hi, %s! Are you registered to vote in %s?" % (self.user_id, self.sms_text))
                return tropo.RenderJson()

            if self.state == 2:
                tropo = Tropo()
                
                if "y" in self.sms_text.lower():
                    # This is where we check if you have a driver license.
                    self.connection.api.find_and_modify(
                        query={"user_id":self.user_id},
                        update={"user_id":self.user_id,"state":0, "geographic_state":None},
                        upsert=True)
                    tropo.say("Congratulations, %s! You can vote! Call (555) 555-5555 for more information." % self.user_id)
                
                elif "n" in self.sms_text.lower():
                    # This is where we check if the voter registration has passed.
                    self.connection.api.find_and_modify(
                        query={"user_id":self.user_id},
                        update={"user_id":self.user_id,"state":0, "geographic_state":None},
                        upsert=True)
                    tropo.say("Your voter registration date has passed, %s. We has a sad." % self.user_id)
                
                else:
                    # We didn't get a yes or a no from the user.
                    tropo.say("We didn't understand your response, %s. Please respond with yes or no." % self.user_id)
                
                return tropo.RenderJson()

    def set_basic_params(self):
        self.user_id = self.data['session']['from']['id']
        self.sms_text = self.data['session']['initialText']

    def get_request(self, request):
        """
        Get the request and turn it into a dictionary.
        """
        return dict(json.loads(request.data))

    def determine_state(self):
        """
        Get this user and determine their state.
        """
        # Find this user.
        state = self.connection.api.find_one({"user_id":self.user_id})

        # If they have a state, return it. Otherwise, return nothing.
        if state:
            return state['state']
        else:
            return 0

@app.route('/helloworld.json', methods=['GET', 'POST'])
def hello():
    tropo = Tropo()
    tropo.say("Hello, World")
    return tropo.RenderJson()

@app.route('/vote.json', methods=['GET', 'POST'])
def vote():
    voter = Voter()
    return voter.run(request)

@app.route('/', methods=['GET'])
def homepage():
    context = {}
    return render_template('index.html', **context)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
