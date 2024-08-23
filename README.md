# Welcome to DUKE Repository!

## Getting Started

The entire project is dockerized. To get started, follow these steps:

1. **Install Docker**: Ensure you have Docker installed on your machine.

2. **Configure Environment Variables**: Create a `.env` file in the root of your project directory with the following
   structure:

   ### .env Template
    ```env
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    DB_NAME=your_db_name
    ```

   ### Description
    - **DB_USER**: The username for your database connection. For example, `"postgres"`.
    - **DB_PASSWORD**: The password for your database connection. For example, `"postgres"`.
    - **DB_HOST**: The hostname for the database service. Use `"database"` as it corresponds to the Docker container
      name.
    - **DB_PORT**: The port number on which your database server listens. For example, `5432`.
    - **DB_NAME**: The name of the database to connect to. For example, `"duke"`.

   These variables configure the PostgreSQL database service that the project will use.
   
   ### Complete .env Example
    ```env
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=database
    DB_PORT=5432
    DB_NAME=duke
    ```

3. **Run `duke-cli`**: To execute the `duke-cli` command, use the following command:

   ### For macOS
    ```bash
    source ./duke-cli.sh
    ```

   For help and usage options, run:
    ```bash
    source ./duke-cli.sh --help
    ```

4. **Run MyPy Tests**: To perform type checking with MyPy, use the following command:
    
    ### For macOS
    ```bash
    source ./mypy-tests.sh
    ```

## Containers Overview

The project includes the following Docker containers:

- **duke-cli**: This container runs the `duke-cli` command-line interface. It is built from the provided `Dockerfile`
  and depends on the `database` container. 

- **duke-database**: This container runs a PostgreSQL database. It is configured with environment variables for database
  credentials and persists data using a Docker volume. It also includes a health check to ensure the database is ready.

## Architecture Overview

The project follows Clean Architecture principles with the following package structure:

- **domain**: Corresponds to the entities/enterprise business rules layer.
- **application**: Corresponds to the use cases/application business rules layer.
- **interface_adapters**: Corresponds to the interface adapters layer.
- **infrastructure**: Corresponds to the frameworks/drivers layer.

## Optional: Virtual Environment Configuration (macOS)

If you'd like to set up a Python virtual environment for local development, follow these steps:

1. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install the Project Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

This setup is useful during development.
