# Data Connector Platform

This is a full-stack web application that allows users to connect to multiple databases, extract data in batches, edit the data in a grid, and send it to a backend for processing and storage.

## Architecture Overview

The application is a monorepo with a Next.js frontend and a Django REST Framework backend. The entire application is containerized using Docker and Docker Compose.

-   **Frontend**: A Next.js application responsible for the user interface, including the data grid for editing data.
-   **Backend**: A Django REST Framework application that provides a RESTful API for managing database connections, extracting data, and processing submitted data.
-   **Databases**:
    -   A PostgreSQL database serves as the primary database for the Django application.
    -   The application can connect to multiple external databases (PostgreSQL, MySQL, MongoDB, ClickHouse) for data extraction.

## Tech Stack Decisions

-   **Frontend**: Next.js was chosen for its server-side rendering capabilities, which can improve performance and SEO, and its rich ecosystem of libraries and tools.
-   **Backend**: Django REST Framework was chosen for its rapid development capabilities, built-in admin interface, and robust ORM.
-   **Containerization**: Docker and Docker Compose were chosen to ensure a consistent development and deployment environment, and to simplify the management of multiple services.

## Database Connector Design

The database connector is designed to be extensible, allowing for the easy addition of new database types. A `DatabaseConnection` model stores the connection details for each database. A `get_connection` utility function provides a simple interface for creating a connection to a database, and an `extract_data` function handles the batch extraction of data.

## Setup Instructions

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd data-connector-platform
    ```
2.  **Set up environment variables**:
    Create a `.env` file in the root of the project and add the following:
    ```
    DATABASE_URL=postgres://user:password@db:5432/dataconnector
    ```
3.  **Build and run the application**:
    ```bash
    docker-compose up --build
    ```
    The frontend will be available at `http://localhost:3000` and the backend at `http://localhost:8000`.

## API Documentation

-   `POST /api/connections/`: Create a new database connection.
-   `GET /api/connections/`: Get a list of all database connections.
-   `POST /api/extract/`: Extract data from a database.
-   `POST /api/submit/`: Submit edited data to the backend.

