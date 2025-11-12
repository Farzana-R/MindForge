import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
import bcrypt

MONGO_URL = "mongodb://mongo:27017"
DB_NAME = "mindforge_db"
COLLECTION = "users"

async def create_admin():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    users_collection = db[COLLECTION]

    # check if admin already exists
    existing_admin = await users_collection.find_one({"email": "admin@mindforge.com"})
    if existing_admin:
        print("⚠️ Admin user already exists:", existing_admin["_id"])
        return

    # password hashing
    plain_password = "Admin@123"   # you can change this
    hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())

    admin_user = {
        "_id": ObjectId(),  # auto-generate ObjectId
        "email": "admin@mindforge.com",
        "first_name": "Aysha",
        "last_name": "K",
        "date_of_birth": datetime(1995, 9, 27),
        "phone_number": "9876566794",
        "address": "123, Park Avenue, Mumbai, India",
        "gender": "female",
        "role": "admin",
        "password": hashed_password.decode("utf-8"),  # save as string
    }

    await users_collection.insert_one(admin_user)
    print("✅ Admin user created successfully with email:", admin_user["email"])
    print("   Login password:", plain_password)


if __name__ == "__main__":
    asyncio.run(create_admin())
