"""
Configuration of 'memos' Flask app. 
Edit to fit development or deployment environment.

"""
import random 

### My local development environment
#PORT=5000
#DEBUG = True
#MONGO_URL = "mongodb://address:enroute@localhost:4260/memos"  

PORT=4567
DEBUG = False # Because it's unsafe to run outside localhost
MONGO_URL =  "mongodb://a:b@ix.cs.uoregon.edu:4260/AddressBook"  # on ix
