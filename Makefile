all:

# docker
up:
	@echo "bringing up project...."
	docker compose up

down:
	@echo "bringing down project...."
	docker compose down

bash:
	@echo "connecting to container...."
	docker compose exec -it hydr_backend bash

# alembic
alembic-scaffold:
	@echo "scaffolding migrations folder..."
	docker compose exec hydr_backend alembic init -t async migrations

alembic-init:
	@echo "initializing first migration...."
	docker compose exec hydr_backend alembic revision --autogenerate -m "init"

alembic-revision:
	@echo "creating migration file...."
	docker compose exec hydr_backend alembic revision --autogenerate -m "add year"

alembic-upgrade:
	@echo "applying migration...."
	docker compose exec hydr_backend alembic upgrade head

# lint
# test:
# 	@echo "running pytest...."
# 	docker compose exec hydr_backend pytest --cov-report xml --cov=src tests/

lint:
	@echo "running ruff...."
	docker compose exec hydr_backend ruff sr

black:
	@echo "running black...."
	docker compose exec hydr_backend black .

mypy:
	@echo "running mypy...."
	docker compose exec hydr_backend mypy src/

# misc
check: BREW-exists
BREW-exists: ; @which brew > /dev/null

hooks: check
	@echo "installing pre-commit hooks...."
	pre-commit install


# можно подключиться к базе данных:
# psql -h 192.168.0.4 -U <user_db> -d <name_container>
