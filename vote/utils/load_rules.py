#!/usr/bin/env python
"""
Load Voting Information Project voter id data into sqlite.
"""
import csv
import glob
import os
import re
import sqlite3
import sys

from vote.libs.states import STATES, STATES_BY_SLUG, STATE_SLUGS_REGEX

def load_voter_id_rules():
    print STATE_SLUGS_REGEX
    sqlite_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
    data_dir = os.path.join(sqlite_dir, 'rotr')
    cnx = sqlite3.connect(os.path.join(sqlite_dir, 'canivote.sqlite'))
    cursor = cnx.cursor()
    # Create rules table if it doesn't exist
    try:
        cursor.execute("CREATE TABLE rules ("
                       "state,"
                       "voter_identification_verified,"
                       "voter_identification_id,"
                       "voter_identification_name)")
        print "Created table rules..."
    except:
        pass

    cursor.execute('delete from rules')
    cnx.commit()

    INSERT = "INSERT INTO rules VALUES (?,?,?,?)"
    # Load data
    payload = []
    for fname in glob.glob(data_dir + '/*.csv'):
        print "Loading %s" % fname
        data = get_data(fname)

        for row in data:
            # Skip blank rows
            if row['voter_identification_verified'].strip():
                payload.append((row['state'], 
                                row['voter_identification_verified'],
                                row['voter_identification_id'],
                                row['voter_identification_name']))

    cursor.executemany(INSERT, payload)
    cnx.commit()
    cnx.close()

def get_data(file_path):
    states_re = re.compile(r'(%s)' % STATE_SLUGS_REGEX)
    fname = file_path.split('/')[-1]
    try:
        state_slug = states_re.match(fname).groups()[0]
        postal = STATES_BY_SLUG[state_slug]
    except (AttributeError, KeyError):
        sys.exit("Unable to find state for %s" % file_path)

    payload = []
    for row in csv.DictReader(open(file_path,'r')):
        row['state']=postal
        payload.append(row)
    return payload

if __name__ == '__main__':
    load_voter_id_rules()
