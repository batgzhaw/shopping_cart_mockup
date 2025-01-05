# Shopping cart minimal example
The respository contains a minimal example of a shopping cart api.  The code is based on the repository https://github.com/caarmen/fastapi-postgres-docker-example. Various
 changes have been made such as moving to SQLModel or adapting to the latest versions of pydantic and FastAPI.
Key features are:

- Implementation based on Docker compose
- A PostgresSQL database in a separate docker container for the purpose of a compact and runnable setup
- A in-memory SQLite database used for integration tests

## Usage
The code requires either an environment or a .env file in the repository root with the 
following environmental variables:

    POSTGRES_SERVER=db
    POSTGRES_PORT=5432
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=app

The application can then be started with :

    docker-compose up

The documentation of the API is available at http://127.0.0.1:8000/docs once the API is running.

The tests can be run by executing pytest in the working directory of the *server* container:

    /usr/src/app pytest


## Remarks

- I chose FastAPI because it provides async and background task capability, native database integration, and a good fit for minimal API applications.
- The Docker Compose setup is intended to provide a single repository implementation of the minimal example that can be easily tested by the reviewers.
- I replaced the use of SQLAlchemy in the boilerplate code because I wanted to be able to reuse the database models as definitions of the request bodies.
- The FastAPI app could be deployed (e.g. on AWS Elastic Beanstalk) by adding a web server like nginx as an additional Docker container.
- The database container should be replaced by an external (managed) database service.
- Similarly, the in-memory SQLite database used in the tests should be replaced by a dedicated
PostgresSQL test database.
- The code does not include any security layers that would need to be added depending on eventual requirements.
- No CI/CD pipeline is defined so far. I would make the decision on which tool to use dependent on the deployment infrastructure.
- No database versioning (alembic) has been included 
