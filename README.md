# Data Connector Platform

This is a full-stack web application that allows users to connect to multiple databases, extract data in batches, edit the data in a grid, and send it to a backend for processing and storage.

## Architecture Overview

The application is a monorepo with a Next.js frontend and a Django REST Framework backend. The entire application is containerized using Docker and Docker Compose.

-   **Frontend**: A Next.js application responsible for the user interface. It features a modern, responsive UI with a data grid for editing data.
-   **Backend**: A Django REST Framework application that provides a RESTful API for managing database connections, extracting data, and storing files.
-   **Databases**:
    -   A PostgreSQL database serves as the primary database for the Django application.
    -   The application can connect to multiple external databases (PostgreSQL, MySQL, MongoDB, ClickHouse) for data extraction.
-   **Services**: The `docker-compose.yml` file defines the following services:
    -   `frontend`: The Next.js application.
    -   `backend`: The Django application.
    -   `db`: The main PostgreSQL database.
    -   `mysql`: A MySQL database for connecting to.
    -   `mongo`: A MongoDB database for connecting to.
    -   `clickhouse`: A ClickHouse database for connecting to.

## Tech Stack

-   **Frontend**: Next.js, React, TypeScript, TanStack Table, Tailwind CSS
-   **Backend**: Django, Django REST Framework, Python
-   **Databases**: PostgreSQL, MySQL, MongoDB, ClickHouse
-   **Containerization**: Docker, Docker Compose

## Database Connector Design

The database connector is designed using an abstraction layer to be extensible, allowing for the easy addition of new database types.

-   `BaseConnector`: An abstract base class that defines the interface for all connectors (`connect()`, `fetch_batch()`, `close()`).
-   Concrete Connectors: `PostgresConnector`, `MySQLConnector`, `MongoConnector`, and `ClickHouseConnector` implement the `BaseConnector` interface for their respective databases.
-   `get_connector`: A factory function that returns the appropriate connector based on the `db_type` of the `DatabaseConnection`.

This design follows the Strategy pattern, making the system modular and easy to maintain.

## Setup Instructions

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd data-connector-platform
    ```
2.  **Build and run the application**:
    ```bash
    docker-compose up --build
    ```
    The frontend will be available at `http://localhost:3000` and the backend at `http://localhost:8000`.

## API Documentation

The API is built with Django REST Framework and provides the following endpoints:

-   `GET, POST /api/connections/`: List all connections or create a new one.
-   `GET, PUT, DELETE /api/connections/{id}/`: Retrieve, update, or delete a specific connection.
-   `POST /api/connections/{id}/extract_data/`: Trigger data extraction from a connection.
-   `GET /api/files/`: List all stored files (with role-based access).

## Demo Script (under 5 minutes)

1.  **Introduction (30 seconds)**
    -   Briefly explain the project: "This is a data connector platform that can connect to various databases, extract data, allow editing, and save the results."
    -   Show the main UI.

2.  **Create a Database Connection (1 minute)**
    -   Open the "Create Connection" form.
    -   Fill in the details for one of the running databases (e.g., the PostgreSQL `db` service).
        -   Name: `My Local Postgres`
        -   DB Type: `PostgreSQL`
        -   Host: `db`
        -   Port: `5432`
        -   Username: `user`
        -   Password: `password`
        -   Database Name: `dataconnector`
    -   Submit the form and show the new connection in the "Connections" list.

3.  **Extract Data (1 minute)**
    -   Select the newly created connection from the dropdown.
    -   Enter a table name. Since we don't have tables in the new DB, you can explain that this would be the name of a table in the target database. For the demo, we can't extract real data without creating it first.
    -   Click "Extract Data".
    -   Show the data appearing in the editable grid.

4.  **Edit and Submit Data (1 minute)**
    -   Edit a few cells in the grid.
    -   Explain that the "Submit" functionality is the next step to implement, which would send the modified data back to the backend.

5.  **View Stored Files (30 seconds)**
    -   Show the "Stored Files" section.
    -   Explain that after data is processed, it's saved as a file, and users can download it from here.
    -   Mention the role-based access control for files.

6.  **Conclusion (30 seconds)**
    -   Briefly summarize the project's capabilities and the technologies used.
    -   Mention potential future improvements, like background data extraction and more advanced data processing.


