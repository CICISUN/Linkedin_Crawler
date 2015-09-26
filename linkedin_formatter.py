__author__ = 'CC'
import logging


logging.getLogger('').handlers = []
LOG_FILENAME = 'master.log'
logging.basicConfig(filename='master.log', level=logging.DEBUG)

import urllib2
import json
from bs4 import BeautifulSoup
from Linkedin_Crawler import linkedin_crawler

firstname='Adam'
lastname='Smith'

#get soup from crawler
candidates_url = linkedin_crawler.get_candidate_urls(firstname, lastname)
logging.info(firstname +", " + lastname + ' has ' + str(len(candidates_url)) + " search result ")


#result containers
candidates=[]
links=[]
headers = { 'User-Agent' : 'Mozilla/5.0' }


#extract uids from url
def get_uid(url):
    if "/in/" in url:
        return url.split("/in/")[1]
    if "/pub/" in url:
        return url.split("/pub/")[1]
    else:
        return  "unknown"


'''
Entity is formatted as a list of complex dictionaries, each dictionary for one candidate
Link is formatted as a list of simple dictionaries, each dictionary records one to one link
'''

#extract profiles
def extract_profiles():
    for i in xrange(len(candidates_url)):
        req = urllib2.Request(candidates_url[i], None, headers)
        profile = urllib2.urlopen(req).read()
        profile_soup = BeautifulSoup(profile, "lxml")
        profile_soup.prettify()

        #profile dict
        candidate={}
        candidate_id = get_uid(candidates_url[i])
        candidate["id"] = candidate_id
        candidate["name"] = firstname + " ," + lastname
        candidate["url"] = candidates_url[i]

        #get headline
        headline=""
        for hdl in profile_soup.findAll('div', id='headline'):
            headline += hdl.text
        candidate["headline"] = headline

        #get description
        description_full=""
        for eachpara in profile_soup.select(".description"):
            description_full = description_full + " " + eachpara.text.replace("\n", "")
        candidate["description"] = description_full

        #get work, postitions
        works=[]
        work_titles=[]
        for work in profile_soup.select(".background-experience"):
            for possible_company in work.findAll('header'):
                for each_company in possible_company:
                    if "h5" in each_company.name:
                        if each_company.text != "":
                           works.append(each_company.text)
                    elif "h4" in each_company.name:
                       work_titles.append(each_company.text)


        candidate["works"] = works
        candidate["work_titles"] = work_titles

        #get friendlist
        friends=[]
        friends_urls=[]
        friend_ids=[]
        for block in profile_soup.select(".insights-browse-map"):
            if "People Also Viewed" in block.find('h3'):
                for friend in block.select("ul li"):
                    possible_friend = friend.find('h4').find('a')
                    possible_friend_url = possible_friend.get('href')
                    possible_friend_id = get_uid(possible_friend_url)
                    friends.append(possible_friend.text)
                    friends_urls.append(possible_friend_url)
                    friend_ids.append(possible_friend_id)
        candidate["friends"] = friends
        candidate["friends_url"] = friends_urls
        candidate["friends_id"] = friend_ids
        candidates.append(candidate)

        #creates links
        for friend in friend_ids:
            link = {}
            joint_id = min(friend, candidate_id) + "->" + max(friend, candidate_id)
            link['id'] = joint_id
            link['candidate'] = candidate_id
            link['friend'] = friend
            links.append(link)

    log_result(candidates)
    link_data = json.dumps(links)
    entity_data = json.dumps(candidates)
    return entity_data, link_data

def log_result(candidates):
    missing_work = 0
    missing_description = 0
    missing_friend = 0
    for candidate in candidates:
        if len(candidate['works']) == 0:
            missing_work+=1
        if len(candidate['friends']) == 0:
            missing_friend+=1
        if candidate['description'] == "" or candidate['description'] is None:
            missing_description+=1
    logging.info(firstname +", " + lastname + ' has ' + str(missing_description) + " entries missing description ")
    logging.info(firstname +", " + lastname + ' has ' + str(missing_work) + " entries missing work experience ")
    logging.info(firstname +", " + lastname + ' has ' + str(missing_friend) + " entries missing friends ")