.PHONY: run lint fmt test docker seed

# -------------------------------------------
# FASTAPI COMMANDS
# -------------------------------------------

run:
	uvicorn app.main:app --reload

# -------------------------------------------
# LINTING & FORMATTING
# -------------------------------------------

lint:
	flake8 .
	black --check .
	isort . --check-only

fmt:
	black .
	isort .

# -------------------------------------------
# TESTING
# -------------------------------------------

test:
	pytest -q

# -------------------------------------------
# DOCKER COMMANDS
# -------------------------------------------

docker:
	docker-compose up --build

docker-down:
	docker-compose down

# -------------------------------------------
# DATABASE SEED
# -------------------------------------------

seed:
	python app/utils/faker_seeder_script.py
