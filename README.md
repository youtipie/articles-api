# Articles API

This is a Flask application that uses SQLAlchemy with PostgreSQL, and Alembic for database migrations. The app provides
an API to manage articles, and tests are written using pytest.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
    - [Environment Variables](#environment-variables)
    - [Build the Docker Environment](#build-the-docker-environment)
    - [Run the Application](#run-the-application)
- [Usage](#usage)
    - [API](#API)
    - [Run the Tests](#run-the-tests)
    - [Loading Initial Data](#loading-initial-data)
    - [Creating users](#creating-users)

## Prerequisites

Before you begin, ensure that the following tools are installed:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.12.4](https://www.python.org/downloads/) (if you prefer to run the app outside Docker)
- [poetry](https://python-poetry.org/docs/) for managing dependencies

## Project Setup

## Environment Variables

The following environment variables are required to configure the application. They can be set in a `.env` file. Example
can be found in a [.env_example](.env_example) file.

* SECRET_KEY: A random secret key used for session management and Flask security features. Leave blank to generate
  random uuid4.
* SQLALCHEMY_TRACK_MODIFICATIONS: Disable Flask-SQLAlchemy event system (set to 0).
* JWT_SECRET_KEY: A secret key for encoding and decoding JWT tokens.
* JWT_ACCESS_TOKEN_EXPIRES_MINUTES: Access token expiration time in minutes.
* JWT_REFRESH_TOKEN_EXPIRES_DAYS: Refresh token expiration time in days.
* PAGE_SIZE: The number of items per page for pagination.
* SQLALCHEMY_DATABASE_URI: The database URI for PostgreSQL. Leave as blank if you are planing to run app with docker.
* POSTGRES_USER: PostgreSQL username. Leave as blank if you are planing to run app locally.
* POSTGRES_PASSWORD: PostgreSQL password. Leave as blank if you are planing to run app locally.
* POSTGRES_DB: PostgreSQL database name. Leave as blank if you are planing to run app locally.

### Build the Docker Environment

To build and run the application in a Docker container, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/youtipie/articles-api.git
   cd articles-api
   ```

2. If Docker is not yet built, build the containers using `docker-compose`:

    ```bash
    docker-compose build
    ```

### Run the Application

After building the Docker containers, you can run the application using Docker Compose:

```bash
docker-compose up
```

This will start the Flask application and the PostgreSQL database in separate containers. By default, the application
will be accessible at http://localhost:8000.

## Usage

### API

Description of all API routes can be found at route `/apidocs`.

### Run the Tests

To run the tests using pytest, follow these steps:

1. Install the necessary dependencies for testing (if not already installed):

    ```bash
    poetry install --with dev
    ```

2. Run the tests:

    ```bash
    poetry run pytest
    ```

## Loading Initial Data

Loading initial data can be done with flask cli command:

```bash
poetry run flask commands prepopulate-db
```

or if you are using app with Docker Compose:

```bash
docker compose exec app poetry run flask commands prepopulate-db
```

This will add few articles and users to your database.

## Creating users

Users can be created with following flask cli command:

```bash
poetry run flask commands create-user --username <username> --pasword <pasword> --role <role>
```

or if you are using app with Docker Compose:

```bash
docker compose exec app poetry run flask commands create-user --username <username> --pasword <pasword> --role <role>
```

Where `--username` is username of the user, `--password` is the password of the user and `--role` is role of the user (
can be admin, editor or viewer)

