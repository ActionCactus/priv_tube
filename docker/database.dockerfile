# Copied and modified from https://github.com/KEINOS/Dockerfile_of_SQLite3/blob/master/Dockerfile
FROM python:latest AS build-env

RUN apt-get update
RUN apt-get install -y sqlite3
RUN sqlite3 --version

# -----------------------------------------------------------------------------
# FROM python:3.8.7-slim

# COPY --from=build-env /usr/bin/sqlite3 /usr/bin/sqlite3

# Create a group and user for SQLite3 to avoid: Dockle CIS-DI-0001
RUN adduser --system --group sqlite

USER sqlite

# Copy code directory
COPY . /app
WORKDIR /app

# Install Python packages for migrations
RUN pip install -r requirements.txt

# Set container's default command as `sqlite3`
CMD ./docker/db_init.sh

# Avoid: Dockle CIS-DI-0006
HEALTHCHECK \
  --start-period=1m \
  --interval=5m \
  --timeout=3s \
  CMD /usr/bin/sqlite3 --version || exit 1