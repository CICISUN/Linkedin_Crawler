__author__ = 'CC'

import urllib2
import json

from bs4 import BeautifulSoup

from Linkedin_Crawler import linkedin_crawler


dummy_firstname='Adam'
dummy_lastname='Smith'

#get soup from crawler
candidates_url = linkedin_crawler.get_candidate_urls(dummy_firstname, dummy_lastname)
candidates={}
headers = { 'User-Agent' : 'Mozilla/5.0' }


#extract uids from url
def get_uid(url):
    if "/in/" in url:
        return url.split("/in/")[1]
    if "/pub/" in url:
        return url.split("/pub/")[1]
    else:
        return  "unknown"
def extract_profiles():
#extract profiles
    for i in xrange(len(candidates_url)):
        req = urllib2.Request(candidates_url[i], None, headers)
        profile = urllib2.urlopen(req).read()
        profile_soup = BeautifulSoup(profile, "lxml")
        profile_soup.prettify()

        #profile dict
        candidate={}
        candidate["id"] = get_uid(candidates_url[i])
        candidate["name"] = dummy_firstname + "," + dummy_lastname
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
        candidates[candidate["id"]] = candidate

    json_string = json.dumps(candidates)
    return json_string

