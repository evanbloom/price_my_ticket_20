
###################
#Date: 3-22-2015
#Author: Evan Bloom
#Summary: This code querries the Stubhub ticketsAPI periodically and downloads all the ticket data
################

import json
from pprint import pprint
import urllib2
import pandas as pd
import xmltodict
from pandas.lib import Timestamp
import datetime
import random
import time

def pull_event_data(event_id):
    url = 'http://www.stubhub.com/ticketAPI/restSvc/event/%s' %event_id
    current_time=datetime.datetime.utcnow()


    #Download Listing of Tickets
    data = json.load(urllib2.urlopen(url))
    tickets = data['eventTicketListing']['eventTicket']

    data_dict = {}
    count=0
    for ticket in tickets:
        ticket_seat = str(ticket['se']).split(',')
        for seat in ticket_seat:
            ticket_info = {}
            ticket_info['ticket_id']= ticket['id']
            ticket_info['ticket_section']= str(ticket['st'])
            ticket_info['ticket_row']= str(ticket['rd'])
            ticket_info['ticket_qt']= str(ticket['qt'])
            ticket_info['ticket_seat']= seat
            ticket_info['price']= ticket['tc']['amount']
            data_dict[count]=ticket_info
            count +=1

    ticket_frame = pd.DataFrame.from_dict(data_dict,orient='index')
    ticket_frame['event_id']= event_id
    ticket_frame['query_time'] = current_time
    return(ticket_frame)


# In[3]:

def grab_data (events_table, random_init=False):
    
    events_table['last_api_call']=None
    file_address = #####Fill in file address here
    file_name = #Fill in file name here
    count= 0
    while keep_pulling:
        try:
            for i in events_table.index:
                current_time= datetime.datetime.utcnow()
                until_game = events_table.time_date[i] - current_time
                time_from_last=  current_time - events_table.last_api_call[i]




                #If no last querry then qury
                if events_table.last_api_call == None:
                    tickets = pull_event_data(events_table.event_id[i])
                    #If Random Init = True, then pause for random amount of time
                    if random_init:
                        time.sleep (int(random.uniform(0,360)))

                #if game is more than 7 days away, pull every 6 hours
                elif until_game.seconds > (60*60*24*7):

                    if time_from_last.seconds > (60*60*6):
                        tickets = pull_event_data(events_table.event_id[i])
                    else: pass

               #if game is between 7 and 1 day away, pull every hour
                elif until_game.seconds()//(60*60*24) > 1:
                    if time_from_last.seconds > (60*60):
                        tickets = pull_event_data(events_table.event_id[i])
                        else: pass
               #if game is less than one day away, pull every five minues
                elif until_game.seconds() >0:
                    if time_from_last.seconds > (60*60):
                        tickets = pull_event_data(events_table.event_id[i])
                else:
                    continue

                file_name = "Part"+str(count).zfill(8)
                file_address = "~/"+datetime.datetime.now().strftime('%Y_%m_%d')
                events_table.last_api_call[i] = current_time
                tickets.to_csv (file_address + file_name ,  sep='\t')
                count +=1 
        
if __name__ == "__main__":
    events_table = pd.read_csv("MLB_all_regseason_games_2015.csv")
    grab_data(events_table, True)