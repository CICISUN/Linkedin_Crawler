__author__ = 'CC'

import urllib2
from bs4 import BeautifulSoup


dummy_firstname='Adam'
dummy_lastname='Smith'


headers = { 'User-Agent' : 'Mozilla/5.0' }

def get_linkedin_searchresult(firstname, lastname):
    req = urllib2.Request('https://www.linkedin.com/pub/dir/?first=' + firstname + '&last=' + lastname + '&search=Search', None, headers)
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page, "lxml")
    return soup

def get_candidate_urls(firstname, lastname):
#extract profile urls
    candidates_url=[]
    soup = get_linkedin_searchresult(firstname, lastname)
    for anchor in soup.select("li.vcard a"):
        if anchor.get('href') is not None:
            candidates_url.append(anchor.get('href'))
    candidates_url = list(set(candidates_url))
    return candidates_url