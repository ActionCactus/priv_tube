setup-dev:
	python -m pip install -r requirements.txt

test:
	python -m pytest

static-analysis:
	./docker/run_static_analysis.sh

full-reset:
	rm -r data/*

init-db:
	touch data/app.db

migrate-new: init-db
	FLASK_APP=priv_tube.database.migration_app DB_LOCATION=../data/app.db python -m flask db migrate --directory ./priv_tube/migrations

migrate-up: init-db
	FLASK_APP=priv_tube.database.migration_app DB_LOCATION=../data/app.db python -m flask db upgrade --directory ./priv_tube/migrations

migrate-down: init-db
	FLASK_APP=priv_tube.database.migration_app DB_LOCATION=../data/app.db python -m flask db downgrade 19c438dc3eb8 --directory ./priv_tube/migrations

seed-new: init-db
	alembic revision
