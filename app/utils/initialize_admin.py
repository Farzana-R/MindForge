import bcrypt
from bson import ObjectId

from app.core.config import settings
from app.core.database import db


async def create_initial_admin():
    """
    Creates the initial admin user on startup ONLY if it doesn't already exist.
    Safe for production (idempotent).
    """
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD

    if not admin_email or not admin_password:
        print(" ADMIN_EMAIL or ADMIN_PASSWORD not set. Skipping admin creation.")
        return

    users_collection = db["users"]

    # Check if admin exists
    existing_admin = await users_collection.find_one({"email": admin_email})
    if existing_admin:
        print(f"Admin already exists ({admin_email}). Skipping creation.")
        return

    # password hashing
    plain_password = admin_password  # you can change this
    hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())

    # Build admin object
    admin_user = {
        "_id": ObjectId(),  # auto-generate ObjectId
        "email": admin_email,
        "first_name": "Admin",
        "last_name": "User",
        "date_of_birth": None,
        "phone_number": None,
        "address": None,
        "gender": "other",
        "role": "admin",
        # "password": hash_password(admin_password),
        "password": hashed_password.decode("utf-8"),  # save as string
    }

    await users_collection.insert_one(admin_user)

    print(f"Admin created successfully: {admin_email}")
