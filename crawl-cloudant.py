import couchdb, json

credentials = json.load(open('credentials.json'))

couch = couchdb.Server("https://%s.cloudant.com"%credentials['username'])
couch.resource.credentials = (credentials['username'],credentials['password'])

for db in couch:
	print db