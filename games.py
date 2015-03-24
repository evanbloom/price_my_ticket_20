
#############
#Date: 3-22-2015
#Author: Evan Bloom
#Summary: This code querries the Stubhub Listing API to generate a list of all major league professional baseball games in the 2015
#         It returns them as a csv file, used in tickets.py 
#This is a test


################

import json
from pprint import pprint
import urllib2
import pandas as pd
import xmltodict
from pandas.lib import Timestamp
import datetime



#List of Majorleague Baseball teams
teams = ['Orioles','Red%20Sox', 'Yankees', 'Rays', 'Blue%20Jays', 'White%20Sox', 'Indians','Tigers', 'Royals',
'Twins','Astros', 'Angels', 'Athletics', 'Mariners','Rangers','Braves','Marlins', 'Mets','Phillies',
'Nationals','Cubs', 'Reds','Brewers', 'Pirates','Cardinals','Diamondbacks', 'Rockies', 'Dodgers', 'Padres','Giants']

#These two strings are the URL of the listing API with a space for the teamname
querryA = "http://www.stubhub.com/listingCatalog/select?q=stubhubDocumentType:event%20AND%20description:"
querryB= "%20AND%20ancestorGenreDescriptions:MLB&indent=on&fl=event_id%20description%20event_date%20venue_name%20timezone"


#This creates a dictionary, grabbing the necessary fields for each team and event, putting them into a python dictionary
events= {}
count=0
for team in teams:
    o=xmltodict.parse(urllib2.urlopen(querryA + team + querryB))
    for element in o['response']['result']['doc']:
        if not("parking" in element['str'][1]['#text'].lower()) and not("spring training" in element['str'][1]['#text'].lower()):
            events[count]= dict([('event_id',element['str'][0]['#text']),
                                 ('event_name',element['str'][1]['#text'][:element['str'][1]['#text'].find("Tickets")]),
                                 ('location', element['str'][2]['#text']),
                                 ('time_date', element['date']['#text']),
                                 ('timezone', element['str'][3]['#text'])
                                 ])
            count += 1 
       
    
#Convert events dictionary to pandas dataframe
events_table= pd.DataFrame.from_dict(events, orient='index', dtype=None)
#Generate home and away tam variables
teams_table = events_table['event_name'].str.split(' at ').apply(pd.Series, 1)
teams_table.columns=['visiting_team', 'home_team']
events_table = pd.concat([events_table,teams_table],axis=1)

#Each game is listed twice (because it querried for each team, and there are two teams in each game). This removes the duplicates
events_table = events_table.drop_duplicates()

#Convert time_date to pd. datetime variable
events_table['time_date'] = pd.to_datetime(events_table.time_date, utc=True)

#Write events table to csv

events_table.to_csv ("MLB_all_regseason_games_2015.csv")

