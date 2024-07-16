import json
import os
from datetime import datetime, date, timedelta
import logging
import requests

password = ""

def initializeVars():
    global password
    if not os.path.exists('./settings.json'):
        initializeJSON()
    with open("./settings.json", 'r') as f:
        data = json.load(f)
        password = data['password']

def initializeJSON():
    data = {}
    data['password'] = input("\nEnter mysql password:\t")
    with open('./settings.json', 'w') as outfile:
        json.dump(data, outfile)

initializeVars()

def generateDates(start_date, end_date):
    dates_list = []
    current_date = start_date
    days= ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    while current_date <= end_date:
        day = {'date': str(current_date.date()).split("-"),
                'weekday': days[current_date.weekday()]}
        dates_list.append(day)
        current_date += timedelta(days=1)  # Increment by one day

    return dates_list

def getListOfDates(n):
    '''
    if n is 0: get start date and end date frm user, then return [{}, {}, ...] where each {} is a specific date
    {
        date: [yyyy, mm, dd], 
        day: weekday
    }
    if n is 1: set start date and ened date as the current date'''
    if n == 0:
        start = input("\nenter start date (included) yyyy-mm-dd:\t".upper())
        end = input("enter end date (included) yyyy-mm-dd:\t".upper())
        start= start.split('-')
        end = end.split("-")
        start_date = datetime(int(start[0]), int(start[1]), int(start[2]))
        end_date = datetime(int(end[0]), int(end[1]), int(end[2]))
    elif n==1:
        start_date = datetime.today()
        end_date = datetime.today()
    else:
        return 0
    return generateDates(start_date, end_date)

