# main.py
from fastapi import FastAPI, HTTPException, Body, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId

# local imports
from accounts_db import get_database, get_collection
from models import UserRegistration


app = FastAPI()

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "webapp"
COLLECTION_NAME = "accounts"


# Registration endpoint
@app.post("/register")
async def register(user: UserRegistration = Body(...)):
    # Check if the username is already taken

    # double await in this case:
        # 1. to get collection
    collection = await get_collection(collection_name=COLLECTION_NAME,
                                      database_name=DATABASE_NAME,
                                      mongo_uri=MONGO_URI)  
        # 2. To get the fetching result
    existing_user = await collection.find_one({"username": user.username})

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
    result = await collection.insert_one(new_user)

    # Return the user ID (optional)
    return {"user_id": str(result.inserted_id)}

