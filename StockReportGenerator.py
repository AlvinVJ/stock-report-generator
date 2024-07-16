import json
import os

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
