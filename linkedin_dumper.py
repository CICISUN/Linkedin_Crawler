__author__ = 'CC'

from pprint import pprint
import logging

LOG_FILENAME = 'master.log'
logging.basicConfig(filename=LOG_FILENAME, filemode='a', level=logging.DEBUG, format='%(filename)s:%(lineno)s %(levelname)s:%(message)s')

import pymongo
from pymongo import Connection
from Linkedin_Crawler import linkedin_formatter
import json


connection = Connection()
db = connection['test']
entity = db.Entity
links = db.Link


data, link = linkedin_formatter.extract_profiles()

try:
    entity.insert(json.loads(data))
except pymongo.errors.DuplicateKeyError as e:
    logging.info(e.details)
    pass

try:
    links.insert(json.loads(link))
except pymongo.errors.DuplicateKeyError as e:
    logging.info(e.details)
    pass

