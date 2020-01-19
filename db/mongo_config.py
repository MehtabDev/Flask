import sys
import traceback

from pymongo import MongoClient


def db_connection():
    """makes the connection to Mongodb."""
    try:
        # Making a connection with MongoClient
        client = MongoClient('localhost', 27017)  # 27017 is the default port number for mongodb
        # database
        db_name = client['FlaskAPI']
        return db_name
    except Exception as err:
        print('Error occured during mongodb db_connection method, Error Details : - ' + str(
            traceback.format_exception(*sys.exc_info())), flush=True)
        return None
