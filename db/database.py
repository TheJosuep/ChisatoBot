import pymongo, os
from dotenv import load_dotenv
from bson import ObjectId

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
    database = connection["discord_server"]
    collection = database["server"]

    # Obtains document id
    result = collection.find_one( { "id_server": str(guild.id) } )
    id = result["_id"]

    collection.find_one_and_update(
        {"_id": ObjectId(id) },
        {"$set":
            {"name": str(guild.name)}
        }
    )

    print(f"[CHISATO_BOT]: Servidor {guild.name} actualizado correctamente.")

# TODO: Get and set prefix functions
# TODO: Classes for organize code

# COMMANDS HELP:
# 
# It's possible to simply use collection.method(), but is recommended to set parameters into separate documents
# 
# When setting a doc = { "element": value }, you can use it as a parameter to make the code clearer
# Even so, the following examples will use the complete methods
# 
# find_one( { "element_in_collection": variable_to_compare_with } ) - returns a document
# insert_one( {"first_element_in_collection": value, "second_element": value} )
# find_one_and_update( {"_id": ObjectId(string) }, { "$operator": {"element_in_collection": value} } )