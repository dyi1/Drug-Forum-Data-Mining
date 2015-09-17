import os
import re
i = 0
import json
import cloudant

keys = json.load(open('cloudant.json','rb'))

# connect to your account
USERNAME = keys['cloudant']["username"]
password = keys['cloudant']["password"]
# in this case, https://garbados.cloudant.com

account = cloudant.Account(USERNAME)

# login, so we can make changes
login = account.login(USERNAME, password)
assert login.status_code == 200
db = account.database('erowid')



# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("archive cleaned"):
    path = root.split('/')
        
    full_drug_experience = ""
    for file in files:            
        wordList = re.sub("[^\w()-]", " ",  os.path.basename(root)).split()
        cool = "archive cleaned/" + os.path.basename(root) + "/" + file
        with open(cool,"r") as fid:
            #print file_experience
            file_experience = fid.read().replace('\n', '')
        doc = db.document(file[0:-4])
        resp = doc.put(params={
        'text': file_experience,
        'drugs': wordList
        })
