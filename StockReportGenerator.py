import json
import os
from datetime import datetime, date, timedelta
import logging
import requests

password = ""

headersNSE = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest'
}

headersBSE = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx'
}

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

def getListOfDates(n, start = 0 , end = 0):
    '''
    if n is 0: get start date and end date frm function call, then return [{}, {}, ...] where each {} is a specific date
    {
        date: [yyyy, mm, dd], 
        day: weekday
    }
    if n is 1: set start date and ened date as the current date'''
    if n == 0:
        #start = input("\nenter start date (included) yyyy-mm-dd:\t".upper())
        #end = input("enter end date (included) yyyy-mm-dd:\t".upper())
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

def GenerateRawDataFileNames(date):
    NseBhav='BhavCopy_NSE_CM_0_0_0_'+date[0]+date[1]+date[2]+"_F_0000.csv"
    NseDeli="MTO_"+date[2]+date[1]+date[0]+".DAT"
    BseBhav = "BhavCopy_BSE_CM_0_0_0_"+date[0]+date[1]+date[2]+"_F_0000.CSV"
    BseDeli="SCBSEALL"+date[2]+date[1]+".TXT"
    return (NseBhav, BseBhav, NseDeli, BseDeli)

def formatURL(date):
        nse_bhav = f"https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{date[0]}{date[1]}{date[2]}_F_0000.csv.zip"
        nse_deli= f'https://nsearchives.nseindia.com/archives/equities/mto/MTO_{date[2]}{date[1]}{date[0]}.DAT'
        bse_bhav = f"https://www.bseindia.com/download/BhavCopy/Equity/BhavCopy_BSE_CM_0_0_0_{date[0]}{date[1]}{date[2]}_F_0000.CSV"
        bse_deli =f'https://www.bseindia.com/BSEDATA/gross/{date[0]}/SCBSEALL{date[2]}{date[1]}.zip'
        return (nse_bhav, bse_bhav, nse_deli, bse_deli)

def downloadRawData(arrayOfDates):
    for day in arrayOfDates:
        date = day['date']
        NseBhavFileName='BhavCopy_NSE_CM_0_0_0_'+date[0]+date[1]+date[2]+"_F_0000.zip"
        NseDeliFileName="MTO_"+date[2]+date[1]+date[0]+".DAT"
        BseBhavFileName = "BhavCopy_BSE_CM_0_0_0_"+date[0]+date[1]+date[2]+"_F_0000.CSV"
        BseDeliFileName="SCBSEALL"+date[2]+date[1]+".zip"
        filenames = (NseBhavFileName, BseBhavFileName, NseDeliFileName, BseDeliFileName)
        urls = formatURL(date)
        types = ['nse_bhav', 'bse_bhav', 'nse_deli', 'bse_deli']

        #downloading data
        for i in range(4):
            url = urls[i]
            filename = filenames[i]
            if i in [0, 1]:
                response= requests.get(url, headers = headersNSE)
            elif i in [2, 3]:
                response= requests.get(url, headers = headersBSE)
            if response.status_code==200:
                with open(f"RawData/{filename}",'wb') as f:
                    f.write(response.content)
            elif response.status_code==404:
                print("no data for " + '-'.join(date) + " "+day['weekday'] + " " + types[i])
            else:
                print(response.status_code)

