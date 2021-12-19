Generic single-database configuration.

# Adding new migrations
```bash
.env/bin/alembic init content_registry_migrations
.env/bin/alembic revision -m"Your change description here"
```