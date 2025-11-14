# 🧠 MindForge - LMS Backend (FastAPI + MongoDB)

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal?logo=fastapi)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-brightgreen?logo=mongodb)](https://www.mongodb.com/)
[![CI](https://img.shields.io/github/actions/workflow/status/Farzana-R/MindForge/ci.yml?label=CI%20Checks)](https://github.com/Farzana-R/MindForge/actions)
[![Code Style: Black](https://img.shields.io/badge/Code%20Style-Black-black?logo=python)](https://github.com/psf/black)
[![Linting: Flake8](https://img.shields.io/badge/Linting-Flake8-red)](https://flake8.pycqa.org/)
[![Imports: isort](https://img.shields.io/badge/Imports-isort-blue)](https://pycqa.github.io/isort/)
[![Pre-commit](https://img.shields.io/badge/Pre--commit-Enabled-orange?logo=precommit)](https://pre-commit.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)


**MindForge** is a modular, secure Learning Management System (LMS) backend built with **FastAPI**, **Motor (MongoDB)**, **JWT authentication**, and modern DevOps practices like **CI/CD pipelines**, **pre-commit hooks**, and **automatic code linting & formatting**.

It is designed for scalability, clean architecture, and production-like workflow.


---

## ✨ Features

### 🔐 Authentication & Authorization  
- Secure JWT login  
- Role-based access (Admin, Instructor, Student)  
- OAuth2PasswordBearer authentication  

### 📚 LMS Features  
- Course CRUD  
- Enrollment system  
- Progress tracking  
- Pagination, searching & filtering  
- MongoDB operations using async Motor  

### 🧪 Developer Experience  
- 🚀 Pre-commit auto linting  
- ✔️ Black (formatter)  
- ✔️ Flake8 (linter)  
- ✔️ isort (import sorter)
- ✔️ GitHub Actions CI pipeline  
- ✔️ Makefile automation  
- 🔄 Docker-based local development  

### 🧰 Extra Tools  
- Faker-based seeder script  
- Modular folder structure  
- Environment-driven configuration 

---

## 🛠 Tech Stack

| Layer        | Tools |
|--------------|-----------------------------------------|
| Backend      | FastAPI |
| Database     | MongoDB + Motor |
| Auth         | JWT, OAuth2 |
| Validation   | Pydantic |
| Dev Tools    | Black, Flake8, isort, Pre-commit |
| CI/CD        | GitHub Actions |
| Container    | Docker + Docker Compose |
---

## 📁 Folder Structure

<pre>
fastapi-lms/
├── app/
│   ├── core/        # DB connection, base configs
│   ├── models/      # MongoDB operations (Motor)
│   ├── routers/     # All API endpoints
│   ├── schemas/     # Pydantic models
│   ├── utils/       # Auth helpers, seeder, utilities
│   ├── dependencies # Role & auth dependencies
├── .github/workflows/ci.yml  # GitHub lint pipeline
├── .pre-commit-config.yaml   # Pre-commit hooks
├── Makefile
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── README.md
└── requirements.txt
</pre>


---

## 🧹 Code Quality & Automation

MindForge enforces consistent, production-level code standards using:

### ✔️ Pre-commit Hooks  
Automatically runs before each commit:

- `black` (formatting)  
- `flake8` (linting)  
- `isort` (import sorting)  
- `end-of-file-fixer`  
- `trailing-whitespace`  

Install Once:

```bash
pre-commit install
```

Run manually:
```bash
pre-commit run --all-files
```

## ✔️ Black — Auto Formatting

Runs automatically or manually:

```bash
black .
```

## ✔️ Flake8 — Linting

Ensure code quality:

```bash
flake8 .
```

## ✔️ isort — Import Ordering

Sort imports consistently:

```bash
isort .
```

## ✔️ CI/CD Pipeline (GitHub Actions)

Every push triggers:

 - Black (check mode)
 - Flake8
 - isort
 - (future) Automated tests


## ✔️ Makefile Commands

```bash
make format   # Run black + isort
make lint     # Run flake8
make run      # Start FastAPI development server
make docker   # Build & run with Docker
make seed     # Seeder script
```

## 🔐 Authentication
### Endpoints

- `POST /users/` — Register user with role
- `POST /auth/login` — Login and receive access token

- Include the token in headers:

Authorization: bearer <your_token_here>

---


## 📘 API Documentation

FastAPI provides automatic Swagger docs:

> 🔗 [http://localhost:8000/docs](http://localhost:8000/docs)
> 🔗 [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⚙️ Environment Variables

Create a `.env` file in the root:

```bash
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=mindforge_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🧪 Seeder - Generate Dummy Data

Use Faker to insert test users & courses:

```bash
python app/utils/faker_seeder_script.py
```


## 📦 Installation (Local Dev)

### Clone the repo
git clone https://github.com/Farzana-R/MindForge.git
cd mindforge

### Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### Install dependencies
pip install -r requirements.txt

### Start the server
uvicorn app.main:app --reload


## 🐳 Docker Setup
```bash
docker-compose up --build
```
Starts:
 - mindforge_api (FastAPI)
 - mindforge_mongo (MongoDB)

With live reload enabled.



## 🧭 Roadmap

  - JWT authentication
  - User roles & permissions
  - Course CRUD
  - Enrollment system
  - Progress tracking
  - Search, filters, pagination
  - Pre-commit + code quality tools
  - Makefile
  - CI pipeline
  - Lesson & quiz modules(need to implement)
  - Admin reporting & analytics (need to implement)
  - Unit tests + CI test pipeline (need to implement)


## 🧪 Testing Scenarios

 - Massive data creation (1000+ users)
 - Role-based restrictions
 - Token expiration behavior
 - Pagination & search combinations
 - Schema validation failures
 - Performance tests on course listing


## 📄 License
This project is licensed under the MIT License

🙋‍♀️ Author
Built by Farzana — Python Developer
🔗 GitHub: https://github.com/Farzana-R • LinkedIn
