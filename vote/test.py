import requests
from unittest import TestCase

class TestX(TestCase):

    def setUp(self):
        p = '{"session":{"from":{"id":"12345"}, "initialText":"clear"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
    
    def test_cant_vote_not_registered(self):
        
        #voter reg in missisiippi has already passed us by
        
        #initial contact
        p = '{"session":{"from":{"id":"12345"}, "initialText":"vote"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Hello! What state do you live in?"}}]}')
        
        #give it a state
        p = '{"session":{"from":{"id":"12345"}, "initialText":"MS"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Are you registered to vote in MS?"}}]}')

        #give it a state
        p = '{"session":{"from":{"id":"12345"}, "initialText":"no"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "You can\'t vote. The deadline for registering to vote has passed. Call (601) 576-2550 with further questions."}}]}')
        
    def test_can_vote_not_registered(self):
        
        #voter reg in missisiippi has already passed us by
        
        #initial contact
        p = '{"session":{"from":{"id":"12345"}, "initialText":"vote"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Hello! What state do you live in?"}}]}')
        
        #give it a state
        p = '{"session":{"from":{"id":"12345"}, "initialText":"NH"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Are you registered to vote in NH?"}}]}')

        #give it a state
        p = '{"session":{"from":{"id":"12345"}, "initialText":"no"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "You still have time to register to vote. The deadline to register is Tuesday, Nov. 6. Call (603) 271-3242 to learn how to register."}}]}')
        
