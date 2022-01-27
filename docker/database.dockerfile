# Copied and modified from https://github.com/KEINOS/Dockerfile_of_SQLite3/blob/master/Dockerfile
FROM python:3.8.7-slim AS build-env

RUN \
  apk add --update \
    alpine-sdk \
    build-base  \
    tcl-dev \
    tk-dev \
    mesa-dev \
    jpeg-dev \
    libjpeg-turbo-dev \
  # Download latest release
  && wget \
    -O sqlite.tar.gz \
    https://www.sqlite.org/src/tarball/sqlite.tar.gz?r=release \
  && tar xvfz sqlite.tar.gz \
  # Configure and make SQLite3 binary
  && ./sqlite/configure --prefix=/usr \
  && make \
  && make install \
  # Smoke test
  && sqlite3 --version \

# -----------------------------------------------------------------------------
# FROM python:3.8.7-slim

# COPY --from=build-env /usr/bin/sqlite3 /usr/bin/sqlite3

# Create a group and user for SQLite3 to avoid: Dockle CIS-DI-0001
ENV \
  USER_SQLITE=sqlite \
  GROUP_SQLITE=sqlite

RUN addgroup -S $GROUP_SQLITE \
  && adduser  -S $USER_SQLITE -G $GROUP_SQLITE

USER $USER_SQLITE

# Install Python packages for migrations
RUN flask db upgrade

# Copy code directory
COPY . /app
WORKDIR /app

# Set container's default command as `sqlite3`
CMD /usr/bin/sqlite3

# Avoid: Dockle CIS-DI-0006
HEALTHCHECK \
  --start-period=1m \
  --interval=5m \
  --timeout=3s \
  CMD /usr/bin/sqlite3 --version || exit 1