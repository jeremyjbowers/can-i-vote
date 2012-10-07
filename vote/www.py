#!/usr/bin/env python
import os

from flask import Flask
from flask import render_template, request
from tropo import Tropo
import json
from mongolier import Connection
from vote.data import api

app = Flask(__name__)

class Voter(object):

    # Set up the mongo connection.
    connection = Connection(db="canivote", collection="users")
    user_id = None
    sms_text = None
    state = None
    data = None

    def run(self, request):

        if request.method == "POST":
            self.data = self.get_request(request)
            self.set_basic_params()
            self.state = self.determine_state()
            
            if self.sms_text == 'clear':
                self.connection.api.find_and_modify(
                    query={"user_id":self.user_id},
                    update={"user_id":self.user_id,"state":0, "geographic_state":None},
                    upsert=True)
                return 'cleared'

            if self.state == 0:
                self.connection.api.find_and_modify(
                    query={"user_id":self.user_id},
                    update={"user_id":self.user_id,"state":1,"geographic_state":None},
                    upsert=True)
                tropo = Tropo()
                tropo.say("Hello! What state do you live in?")
                return tropo.RenderJson()

            if self.state == 1:
                self.connection.api.find_and_modify(
                    query={"user_id":self.user_id},
                    update={"user_id":self.user_id,"state":2,"geographic_state":self.sms_text},
                    upsert=True)
                tropo = Tropo()
                tropo.say("Are you registered to vote in %s?" % (self.sms_text))
                return tropo.RenderJson()

            if self.state == 2:
                tropo = Tropo()
                
                geographic_state = self.get_geographic_state()
                state_phone_number = api.elec_agency_phone(geographic_state)
                
                if "yes" in self.sms_text.lower():
                    #is this a voter id state?
                    
                    if api.is_id_required(geographic_state):
                        #yes, then we ask for forms of ID
                        #TODO:SERDAR, what's the first valid form of ID?
                        first_valid_id = api.primary_form_of_id(geographic_state)
                        
                        self.connection.api.find_and_modify(
                            query={"user_id":self.user_id},
                            update={"user_id":self.user_id,"state":3,"geographic_state":self.sms_text},
                            upsert=True)
                        tropo = Tropo()
                        tropo.say("Do you have a %s?" % (first_valid_id))
                        return tropo.RenderJson()
                        
                    else:                    
                        #no, then they can vote
                        self.connection.api.find_and_modify(
                            query={"user_id":self.user_id},
                            update={"user_id":self.user_id,"state":0, "geographic_state":None},
                            upsert=True)
                        tropo.say("You can vote! Call %s for more information." % state_phone_number)
                
                elif "no" in self.sms_text.lower():
                    # This is where we check if the voter registration has passed.
                    still_time_to_register = api.has_voting_deadline_passed(geographic_state)
                    deadline_to_register = api.get_voting_deadline(geographic_state)
                    
                    if still_time_to_register:
                        self.connection.api.find_and_modify(
                            query={"user_id":self.user_id},
                            update={"user_id":self.user_id,"state":0, "geographic_state":None},
                            upsert=True)
                        tropo.say("You still have time to register to vote. The deadline to register is %s. Call %s to learn how to register." % (deadline_to_register,state_phone_number))
                    else:
                        self.connection.api.find_and_modify(
                            query={"user_id":self.user_id},
                            update={"user_id":self.user_id,"state":0, "geographic_state":None},
                            upsert=True)
                        tropo.say("You can\'t vote. The deadline for registering to vote has passed. Call %s with further questions." % state_phone_number)
                
                else:
                    # We didn't get a yes or a no from the user.
                    tropo.say("We didn't understand your response, %s. Please respond with yes or no." % self.user_id)
                
                return tropo.RenderJson()
                
            else:
                tropo.say("Sorry, we're not done with this part.")
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
            
    def get_geographic_state(self):
        """
        Get this user and determine their state.
        """
        # Find this user.
        state = self.connection.api.find_one({"user_id":self.user_id})

        # If they have a state, return it. Otherwise, return nothing.
        if state:
            return state['geographic_state']
        else:
            return ""

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
