#!/usr/bin/env python
"""
Data access for Can I Vote.

USAGE

>>> from vote.data import api
>>> api.has_voting_deadline_passed('TN')

"""
import datetime
import os
from sqlalchemy import create_engine, select, Table, MetaData

class QueryAPI(object):

    def __init__(self):
        self.sqlite_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
        self.engine = create_engine('sqlite:///%s' % self.sqlite_db)
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)

    def has_voting_deadline_passed(self, state):
        """
        >>> from vote.data import api
        >>> api.has_voting_deadline_passed('CA')
        True

        """
        tbl = self.meta.tables['voting_cal']
        query = select([tbl.c.registration_deadline], tbl.c.state_postal == state)
        # Short circuit if state is North Dakota, which has no registration deadline
        if state == 'ND':
            return False
        deadline = self.engine.execute(query).fetchone()[0]
        
        if deadline > datetime.date.today():
            return True
        else:
            return False
            
    def get_voting_deadline(self, state):
        """
        >>> from vote.data import api
        >>> api.has_voting_deadline_passed('CA')
        True

        """
        tbl = self.meta.tables['voting_cal']
        query = select([tbl.c.registration_deadline], tbl.c.state_postal == state)
        # Short circuit if state is North Dakota, which has no registration deadline
        if state == 'ND':
            return False
        deadline = self.engine.execute(query).fetchone()[0]
        return deadline

    def elec_agency_phone(self, state):
        """
        >>> from vote.data import api
        >>> api.elec_agency_phone('CA')
        """
        tbl = self.meta.tables['voting_cal']
        query = select([tbl.c.sos_phone], tbl.c.state_postal == state)
        return self.engine.execute(query).fetchone()[0]

api = QueryAPI()
