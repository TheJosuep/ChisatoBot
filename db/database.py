import pymongo, os
from dotenv import load_dotenv

# DB

load_dotenv()
dbUri = os.getenv("DB_URI")

# FUNCTIONS

def DBConnect():
    connection = pymongo.MongoClient(dbUri)
    return connection

# Check if the server already exists in the database and returns a boolean
def VerifyServer(connection, guild):
    database = connection["discord_server"]
    collection = database["server"]
    doc = collection.find_one({"id_server": str(guild.id)})

    if doc:
        return True
    else:
        return False

# Register server in the database when the bot joins for the first time
def RegisterServer(connection, guild):
    database = connection["discord_server"]
    collection = database["server"]
    doc = {"id_server": str(guild.id), "server_name": str(guild.name), "prefix": "c."}
    
    collection.insert_one(doc)

# Update server information in the database when the bot joins
def UpdateServer(connection, guild):
    conn = connection
    gui = guild

# TODO: Get and set prefix functions
# TODO: Classes for organize code