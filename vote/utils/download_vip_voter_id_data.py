#!/usr/bin/env python
"""
Load Voting Information Project voter id data into sqlite.
"""
from bs4 import BeautifulSoup
import csv
import os
import urllib

#from states import STATES
#import pdb;pdb.set_trace()

def download_csv():
    url = "http://data.votinginfoproject.org/rotr/CSV/"
    soup = BeautifulSoup(urllib.urlopen(url).read())
    file_names = [link.attrs['href'] for link in soup.findAll(class_='file') 
                  if 'voter_id' in link.attrs['href']]

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
    for fname in file_names:
        target = os.path.join(data_dir, fname)
        urllib.urlretrieve(url + fname, target)
        print "Downloaded %s" % target

if __name__ == '__main__':
    #main()
    download_csv()
