import os
from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json

app = Flask( __name__ )

#MONGODB_HOST = 'localhost'
#MONGODB_PORT = 27017
#DBS_NAME = 'donorsUSA'gf

COLLECTION_NAME = 'projects'
MONGO_URI = os.getenv('mongodb://root:Abbie!123@ds113282.mlab.com:13282/heroku_xjnbch68', 'mongodb://localhost:27017')
DBS_NAME = os.getenv('heroku_xjnbch68', 'donorsUSA')


@app.route( "/" )
def index():
    """
    A Flask view to serve the main dashboard page.
    """
    return render_template( "index.html" )


@app.route( "/donorsUS/projects" )
def donor_projects():
    """
    A Flask view to serve the project data from
    MongoDB in JSON format.
    """

    # A constant that defines the record fields that we wish to retrieve.
    FIELDS = {
        '_id': False, 'funding_status': True, 'school_state': True,
        'resource_type': True, 'poverty_level': True,
        'date_posted': True, 'total_donations': True
    }

    # Open a connection to MongoDB using a with statement such that the
    # connection will be closed as soon as we exit the with statement
    # The MONGO_URI connection is required when hosted using a remote mongo db.
    with MongoClient( MONGO_URI ) as conn:
        # Define which collection we wish to access
        collection = conn[DBS_NAME][COLLECTION_NAME]
        # Retrieve a result set only with the fields defined in FIELDS
        # and limit the the results to a lower limit of 20000
        projects = collection.find( projection=FIELDS, limit=20000 )
        # Convert projects to a list in a JSON object and return the JSON data
        return json.dumps( list( projects ) )


if __name__ == "__main__":
    app.run( debug=True )