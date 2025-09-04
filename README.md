# 🧠 MindForge - LMS Backend (FastAPI + MongoDB)

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal?logo=fastapi)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-brightgreen?logo=mongodb)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MindForge** is a modular, secure Learning Management System (LMS) backend built using FastAPI and MongoDB.  
It supports user registration, role-based access, JWT authentication, and will scale to handle course and quiz management for thousands of users.

---

## ✨ Highlights

- 🔐 Secure user registration & login with hashed passwords
- 🧾 JWT-based authentication with token expiration
- 📁 MongoDB integration with async support (Motor)
- 🧩 Modular code architecture for scalability
- 🧪 Seeder script for generating test data with Faker

---

## 🛠 Tech Stack

- **Backend:** FastAPI
- **Database:** MongoDB (Motor async driver)
- **Auth:** JWT tokens, Passlib (bcrypt)
- **Validation:** Pydantic
- **Testing Data:** Faker
- **Containerization:** Docker

---

## 📁 Folder Structure

<pre>
fastapi-lms/
├── app/
│   ├── core/       # DB connection & config
│   ├── models/     # MongoDB operations
│   ├── routers/    # API endpoints (modular)
│   ├── schemas/    # Pydantic models
│   ├── utils/      # Auth, seeders
├── .env
├── requirements.txt
├── README.md
</pre>

---

## 🔐 Authentication

- `POST /users/` — Register user with role
- `POST /auth/login` — Login and receive access token
- Include the token in headers:


Authorization: bearer <your_token_here>

---


## 📘 API Docs

FastAPI provides automatic Swagger docs:

> 🔗 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⚙️ Environment Variables

Create a `.env` file in the root:


MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=mindforge_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


---

## 🧪 Seed Dummy Data

Use Faker to insert test users & courses:

```bash
python app/utils/faker_seeder_script.py



📦 Installation (Local Dev)

# Clone the repo
git clone https://github.com/Farzana-R/MindForge.git
cd mindforge

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload


🧭 Roadmap
 User registration & JWT login

 Role-based route restrictions (admin, instructor, student)

 Course, Quiz & Lesson CRUD

 Search and filters

 Docker + Docker Compose

 Data aggregations & reporting

 Unit & integration testing

 Swagger + Postman collections


🧪 Testing Scenarios
Create 1000+ fake users (students + instructors)

Login and test protected routes via Swagger

Validate token expiration, role checks

Test schema validation failures


📄 License
This project is licensed under the MIT License

🙋‍♀️ Author
Built with ❤️ by Farzana — Python Developer & FastAPI Learner
🔗 GitHub Profile • LinkedIn