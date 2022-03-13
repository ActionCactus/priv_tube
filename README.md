# PROOF OF CONCEPT

# priv_tube
A simple, private content sharing system for use by small groups of people.  The goal is to provide users the ability to link their own, private media servers in to a network which offers access control rules in addition to useful features like search and simple community capabilities, like view counts and comments.

# For System Administrators
## First Deployment
The first deployment of the application requires some setup in order to create necessary administrative accounts for all services.  Web application data is currently configured to go in the `./data` folder (this should be changed to the [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html) for the default in the future, and we can provide Windows users with customization options should they want them).

### Runbook

#### Spin Up Application
1.  Build the app image with `docker-compose build app`
2.  Deploy the app with `docker-compose run --service-ports app` and wait until you are prompted to configure the environment

#### Set Up Authentication
3.  Import the Keycloak configuration found at `./resources/system/keycloak/realm-export.json` (overwrite if a resource exists)
4.  Ensure the following realms exist by hovering over the current realm name (`Master`) in the upper left hand corner:
    1.  `Admin`
    2.  `System`
    3.  `User`
5.  Select the `Master` realm and modify the admin password (be sure to store this in a secure password database, such as [Keepass](https://keepass.info/))

## Running
```bash
docker-compose build app
docker-compose run --service-ports app
```

Or, if you're running without Docker (not recommended - all services required for the system to run are configured to be spun up via docker-compose):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m priv_tube.api
```


# For Developers
## The Makefile
We have a Makefile created in the root of this directory for storing and executing commonly used commands.

## Conventions
We are using the PEP8 formatting standard.

## Modifying The Template Database
We use flask-migrate to manage all of our database migrations, and it in turn uses alembic.
When you create or modify a SQLAlchemy model, run `flask db migrate -m"your migration name here"` from the `/priv_tube/cms/db` folder to generate a new migration bringing in your changes.
When you need to create a new custom migration (to do something like generate a seed or create a stored procedure), instead run `alembic revision -m"your migration name here"` from the `/priv_tube/cms/db/migrations`.

To upgrade/downgrade the db, run `flask db upgrade/downgrade` locally (if you're working with it directly instead of using the docker image);

In both of the above scenarios, you will need to commit all the generated files.

## Updating The Template Keycloak Configuration
Run `docker-compose run export_keycloak` and then copy the contents of the JSON file generated in `./data/keycloak_export` to the template in `./resources/system/keycloak/keycloak-export.json`.

# Definition of Terms

* A _content network_ is a collection of servers which are configured to host and share content via Content Management APIs.

# Design
![High Level Overview](resources/design/HighLevelOverview.png)

The system can be thought of as two distinct parts: a content management component and a user application.

## Content Management
### Content Store
The service which houses the shareable content itself.  Initial iterations of this will just be a filesystem, but as the needs arise this can be scaled to include a variety of media hosting technologies.  This should be strictly locked down for security and containment purposes; the only system which should be able to issue commands to the Content Store should be the Content Management API.

### Content Management API
This is the one and only thing which will be able to operate on the content store.  This will handle access control rules and issue commands to the store itself in order to add, update, and delete content.  REPL apps for local management should go through this as well.  Over the long term we can break EAC out in to a separate authentication service should the needs arise.

### Content Registry
This is a database which contains listings for each piece of content stored within the content network.  This is updated by the content manager through scheduled jobs which reach out to all the configured Content Management APIs in order to fetch the latest list of configured media.

### Content Manager
The application layer.  This does the bulk of the work - it manages its local Content Registry through scheduled update jobs, it provides search functionality to the Web App, and it orchestrates forwarding of media from the Content Management API to the Web App and back to the client.

## Web Application
## Web App
This is the client and server for the simple web application which is the user-facing portion of this service.  Aside from GUI features (IE: the client), this should be a very bare-bones portion of the application.  All real functionality should be delegated to the other services described above.
