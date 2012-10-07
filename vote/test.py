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

        #give it a yes or no
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

        #give it a yes or no
        p = '{"session":{"from":{"id":"12345"}, "initialText":"no"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "You still have time to register to vote. The deadline to register is Tuesday, Nov. 6. Call (603) 271-3242 to learn how to register."}}]}')

    def test_can_vote_registered_no_voter_id(self):
        #Alabama

        #initial contact
        p = '{"session":{"from":{"id":"12345"}, "initialText":"vote"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Hello! What state do you live in?"}}]}')
        
        #give it a state
        p = '{"session":{"from":{"id":"12345"}, "initialText":"AL"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Are you registered to vote in AL?"}}]}')

        #give it a yes or no
        p = '{"session":{"from":{"id":"12345"}, "initialText":"yes"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "You can vote! Call (334) 242-7210 for more information."}}]}')
        
    def test_can_vote_registered_voter_id_has_drivers_license(self):
        #Alaska

        #initial contact
        p = '{"session":{"from":{"id":"12345"}, "initialText":"vote"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Hello! What state do you live in?"}}]}')
        
        #give it a state
        p = '{"session":{"from":{"id":"12345"}, "initialText":"AK"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Are you registered to vote in AK?"}}]}')

        #give it a yes or no
        p = '{"session":{"from":{"id":"12345"}, "initialText":"yes"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Do you have a state-issued driver\'s license?"}}]}')

        #give it a yes or no
        p = '{"session":{"from":{"id":"12345"}, "initialText":"yes"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "You can vote! Call (907) 375-6400 for more information."}}]}')

    def test_can_vote_registered_voter_id_no_drivers_license_yes_other_id(self):
        #Arizona

        #initial contact
        p = '{"session":{"from":{"id":"12345"}, "initialText":"vote"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Hello! What state do you live in?"}}]}')
        
        #give it a state
        p = '{"session":{"from":{"id":"12345"}, "initialText":"AZ"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Are you registered to vote in AZ?"}}]}')

        #give it a yes or no
        p = '{"session":{"from":{"id":"12345"}, "initialText":"yes"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Do you have a state-issued driver\'s license?"}}]}')

        #give it a yes or no
        p = '{"session":{"from":{"id":"12345"}, "initialText":"no"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Do you have any of these? Valid Arizona driver\'s license; Valid Arizona non-driver identification; Tribal enrollment card or other form of tribal identification; Valid U.S. federal, state or local government issued identification; Utility bill dated within 90 days of the election; Bank or credit union statement dated within 90 days of the election; Valid Arizona vehicle registration; Indian census card; Property tax statement; Vehicle insurance card; Recorder\'s Certificate"}}]}')

        #give it a yes or no
        p = '{"session":{"from":{"id":"12345"}, "initialText":"yes"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "You can vote! Call (602) 542-4285 for more information."}}]}')

    def test_can_vote_registered_voter_id_no_drivers_license_or_other_id(self):
        #Arizona

        #initial contact
        p = '{"session":{"from":{"id":"12345"}, "initialText":"vote"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Hello! What state do you live in?"}}]}')
        
        #give it a state
        p = '{"session":{"from":{"id":"12345"}, "initialText":"AZ"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Are you registered to vote in AZ?"}}]}')

        #give it a yes or no
        p = '{"session":{"from":{"id":"12345"}, "initialText":"yes"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Do you have a state-issued driver\'s license?"}}]}')

        #give it a yes or no
        p = '{"session":{"from":{"id":"12345"}, "initialText":"no"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "Do you have any of these? Valid Arizona driver\'s license; Valid Arizona non-driver identification; Tribal enrollment card or other form of tribal identification; Valid U.S. federal, state or local government issued identification; Utility bill dated within 90 days of the election; Bank or credit union statement dated within 90 days of the election; Valid Arizona vehicle registration; Indian census card; Property tax statement; Vehicle insurance card; Recorder\'s Certificate"}}]}')

        #give it a yes or no
        p = '{"session":{"from":{"id":"12345"}, "initialText":"no"}}'
        r = requests.post('http://localhost:5000/vote.json',data=p)
        self.assertEqual(r.text,u'{"tropo": [{"say": {"value": "You can\'t vote. Call (602) 542-4285 for more information."}}]}')
