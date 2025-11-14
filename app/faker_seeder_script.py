"""Faker Seeder Script for MindForge LMS
(Python + Motor)"""

import asyncio
import random
from datetime import datetime, timezone

import bcrypt
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient

fake = Faker()

MONGO_URI = "mongodb://mongo:27017"
DB_NAME = "mindforge_db"

NUM_USERS = 1000
NUM_COURSES = 1000


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
    password_hash = bcrypt.hashpw(
        password_plain.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    num_instructors = int(NUM_USERS * 0.3)  # 30% instructors
    num_students = NUM_USERS - num_instructors  # 70% students

    # Generate instructors
    instructor_docs = []
    for _ in range(num_instructors):
        email = fake.unique.email()
        instructors.append(email)
        instructor_docs.append(
            {
                "email": email,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "date_of_birth": fake.date_of_birth(
                    minimum_age=25, maximum_age=50
                ).isoformat(),
                "phone_number": fake.numerify("##########"),
                "address": fake.address(),
                "gender": random.choice(["male", "female"]),
                "role": "instructor",
                "password": password_hash,
            }
        )

    if instructor_docs:
        await users_collection.insert_many(instructor_docs)

    # Generate students
    student_docs = []
    for _ in range(num_students):
        email = fake.unique.email()
        students.append(email)
        student_docs.append(
            {
                "email": email,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "date_of_birth": fake.date_of_birth(
                    minimum_age=18, maximum_age=35
                ).isoformat(),
                "phone_number": fake.numerify("##########"),
                "address": fake.address(),
                "gender": random.choice(["male", "female"]),
                "role": "student",
                "password": password_hash,
            }
        )
    if student_docs:
        await users_collection.insert_many(student_docs)

    # Generate courses — multiple per instructor
    course_categories = [
        "Programming",
        "Design",
        "Marketing",
        "Data Science",
        "Web Development",
    ]
    course_docs = []

    for _ in range(NUM_COURSES):
        instructor_email = random.choice(instructors) if instructors else None
        course_docs.append(
            {
                "title": fake.sentence(nb_words=5),
                "description": fake.paragraph(),
                "category": random.choice(course_categories),
                "instructor": instructor_email,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        )
    if course_docs:
        await courses_collection.insert_many(course_docs)

    print(
        (
            f"Inserted {num_instructors} instructors, "
            f"{num_students} students, "
            f"{NUM_COURSES} courses."
        )
    )


if __name__ == "__main__":
    asyncio.run(seed())
