from motor.motor_asyncio import AsyncIOMotorClient


# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "webapp"
COLLECTION_NAME = "accounts"


# MongoDB connection setup
async def get_database(database_name: str = DATABASE_NAME, 
                       mongo_uri: str = MONGO_URI):
    client = AsyncIOMotorClient(mongo_uri)
    database = client[database_name]
    return database

async def get_collection(collection_name: str = COLLECTION_NAME, 
                         database_name: str = DATABASE_NAME, 
                         mongo_uri: str = MONGO_URI):
    database = await get_database()
    collection = database[COLLECTION_NAME]
    return collection