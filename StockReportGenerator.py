import json
import os

password = ""

def initializeVars():
    global password
    with open("./settings.json", 'r') as f:
        data = json.load(f)
        password = data['password']

def initializeJSON():
    data = {
        "mysqlPassword" : "" 
    }
    data['password'] = input("\nEnter mysql password:\t")
    with open('./settings.json', 'w') as outfile:
        json.dump(data, outfile)


if not os.path.exists('./settings.json'):
    initializeJSON()
else:
    initializeVars()
