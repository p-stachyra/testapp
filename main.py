# main.py
from fastapi import FastAPI, HTTPException, Body, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "webapp"
COLLECTION_NAME = "accounts"

# Pydantic model for user registration
class UserRegistration(BaseModel):
    username: str
    password: str

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

# Registration endpoint
@app.post("/register")
async def register(user: UserRegistration = Body(...)):
    # Check if the username is already taken
    collection_data = await get_collection()
    existing_user = await collection_data.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="Username already registered")

    # Hash the password (you should use a proper password hashing library)
    hashed_password = user.password  # Replace this with actual password hashing

    # Create a new user document
    new_user = {
        "username": user.username,
        "password": hashed_password,
    }

    # Insert the user document into the MongoDB collection
    result = await (await get_collection().insert_one(new_user))

    # Return the user ID (optional)
    return {"user_id": str(result.inserted_id)}
