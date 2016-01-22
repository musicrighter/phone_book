"""
Flask web app connects to Mongo database.

Representation conventions for dates: 
   - In the session object, date or datetimes are represented as
   ISO format strings in UTC.  Unless otherwise specified, this
   is the format passed around internally. Note that ordering
   of ISO format strings is consistent with date/time order
   - User input/output is in local (to the server) time
   - Database representation is as MongoDB 'Date' objects
   Note that this means the database may store a date before or after
   the date specified and viewed by the user, because 'today' in
   Greenwich may not be 'today' here. 
"""

import flask
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we may still need time
from dateutil import tz  # For interpreting local times

# Mongo database
from pymongo import MongoClient

from bson import ObjectId

###
# Globals
###
import CONFIG

app = flask.Flask(__name__)

try: 
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.AddressBook
except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

import uuid
app.secret_key = str(uuid.uuid4())

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  flask.session['books'] = get_books()
  return flask.render_template('index.html')


@app.route("/create_contact")
def create_contact():
    app.logger.debug("Create")
    return flask.render_template('create.html')


@app.route("/_add_book")
def add_book():
    book_name = request.args.get('book_name', 0, type=str)
    
    db[book_name].insert({"a" : "a"})


    return flask.render_template('index.html')


@app.route("/_add_contact")
def add_contact():
    first_name = request.args.get('first_name', 0, type=str)
    last_name = request.args.get('last_name', 0, type=str)
    phone = request.args.get('phone', 0, type=str)
    email =  request.args.get('email', 0, type=str)
    street_address = request.args.get('street_address', 0, type=str)
    city = request.args.get('city', 0, type=str)
    state = request.args.get('state', 0, type=str)
    zipcode = request.args.get('zipcode', 0, type=str)

    put_memo(first_name, last_name, phone, email, street_address, city, state, zipcode)

    return flask.redirect(url_for('index'))


@app.route("/_del_entry")
def del_entry():
    memo_id = request.args.get('_id', 0, type=str)
    collection.remove({'_id': ObjectId(memo_id)})
    return flask.redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#############
#
# Functions available to the page code above
#
##############
def get_contacts():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "contacts" } ).sort("date", 1):
        record['date'] = arrow.get(record['date']).isoformat()
        record["_id"] = str(record["_id"])
        records.append(record)
    return records 

def get_books():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in db.collection_names():
        records.append(record)
    return records 

def put_entry(address_book, first_name, last_name, phone, email, street_address, city, state, zipcode):
    """
    Place contact into database
    """
    try: 
        collection = db.address_book
    except:
        print("Failure opening database")
        sys.exit(1)

    record = { "type": "contact",
               "first_name": first_name,
               "last_name": last_name,
               "phone": phone,
               "email": email,
               "street_address": street_address, 
               "city": city,
               "state": state,
               "zipcode": zipcode 
            }
    collection.insert(record)
    return 


if __name__ == "__main__":
    # App is created above so that it will
    # exist whether this is 'main' or not
    # (e.g., if we are running in a CGI script)
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    # We run on localhost only if debugging,
    # otherwise accessible to world
    if CONFIG.DEBUG:
        # Reachable only from the same computer
        app.run(port=CONFIG.PORT)
    else:
        # Reachable from anywhere 
        app.run(port=CONFIG.PORT,host="0.0.0.0")

    
