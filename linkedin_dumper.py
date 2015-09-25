__author__ = 'CC'

from pprint import pprint

from Linkedin_Crawler import linkedin_formatter

#
# connection = Connection()
# db = connection['test-database']


data = linkedin_formatter.extract_profiles()
pprint(data)