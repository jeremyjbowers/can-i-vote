#!/usr/bin/env python
"""
Data access for Can I Vote.

USAGE

>>> from vote.data import api
>>> api.has_voting_deadline_passed('TN')
False

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
        state = state.upper()
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
        >>> api.get_voting_deadline('CA')
        datetime.date(2012, 10, 22)

        """
        state = state.upper()
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
        >>> api.elec_agency_phone('TX')
        u'(512) 463-5650'

        """
        state = state.upper()
        tbl = self.meta.tables['voting_cal']
        query = select([tbl.c.sos_phone], tbl.c.state_postal == state)
        return self.engine.execute(query).fetchone()[0]

    def is_id_required(self, state):
        """
        >>> from vote.data import api
        >>> api.is_id_required('TX')
        False

        """
        tbl = self.meta.tables['id_required']
        query = select([tbl.c.voter_id_state], tbl.c.state_postal == state)
        return bool(self.engine.execute(query).fetchone()[0])

    def primary_form_of_id(self, state):
        """
        >>> from vote.data import api
        >>> api.primary_form_of_id('TX')
        u"State-issued driver's license"

        """
        tbl = self.meta.tables['rules']
        query = self.engine.execute(select([tbl.c.voter_identification_id, tbl.c.voter_identification_name], tbl.c.state == state))
        data = sorted([(int(row[0]), row[1]) for row in query.fetchall()])
        return data[0][1]

    def other_acceptable_ids(self, state):
        """
        >>> from vote.data import api
        >>> api.other_acceptable_ids('TX')[:13]
        u'Existing law:'

        """
        tbl = self.meta.tables['rules_if_no_id']
        query = select([tbl.c.acceptable_forms_of_id], tbl.c.state_postal == state)
        return self.engine.execute(query).fetchone()[0]

api = QueryAPI()
