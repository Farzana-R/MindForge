"""Faker Seeder Script for MindForge LMS
      (Python + Motor)"""
import asyncio
import random
from datetime import datetime, timezone
from faker import Faker
import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient


fake = Faker()

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "mindforge_db"

NUM_INSTRUCTORS = 10
NUM_STUDENTS = 50

async def seed():
    """Seed the database with fake users and courses."""
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    users_collection = db.users
    courses_collection = db.courses

    # Clear existing fake users (except admins) & courses
    await users_collection.delete_many({"role": {"$in": ["student", "instructor"]}})
    await courses_collection.delete_many({})

    instructors = []
    students = []

    # Password hash
    password_plain = "Test@123"
    password_hash = bcrypt.hashpw(password_plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Generate instructors
    for _ in range(NUM_INSTRUCTORS):
        email = fake.unique.email()
        instructors.append(email)
        await users_collection.insert_one({
            "email": email,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": fake.date_of_birth(minimum_age=25, maximum_age=50).isoformat(),
            "phone_number": fake.phone_number(),
            "address": fake.address(),
            "gender": random.choice(["male", "female"]),
            "role": "instructor",
            "password": password_hash
        })

    # Generate students
    for _ in range(NUM_STUDENTS):
        email = fake.unique.email()
        students.append(email)
        await users_collection.insert_one({
            "email": email,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=35).isoformat(),
            "phone_number": fake.numerify("##########"),
            "address": fake.address(),
            "gender": random.choice(["male", "female"]),
            "role": "student",
            "password": password_hash
        })


    # Generate courses — multiple per instructor
    course_categories = ["Programming", "Design", "Marketing", "Data Science", "Web Development"]
    total_courses = 0

    for instructor_email in instructors:
        num_courses = random.randint(1, 5)  # Each instructor makes 1-5 courses
        for _ in range(num_courses):
            await courses_collection.insert_one({
                "title": fake.sentence(nb_words=5),
                "description": fake.paragraph(),
                "category": random.choice(course_categories),
                "instructor": instructor_email,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            })
            total_courses += 1

    print(
        f"Inserted {NUM_INSTRUCTORS} instructors, {NUM_STUDENTS} students, {total_courses} courses."
        )

if __name__ == "__main__":
    asyncio.run(seed())
