# Incident Tracking API

A backend REST API for incident tracking built with **FastAPI** and **PostgreSQL**. This project supports core issue and user management workflows through CRUD operations, input validation, filtering, and relational database design.

The system was designed to simulate a lightweight backend service that could support internal incident reporting and tracking. It demonstrates backend engineering fundamentals including API design, database integration, schema constraints, nullable relationships, and update/delete workflows.

## Features

- User management (create, retrieve users)
- Issue tracking system with full CRUD operations
- Filtering issues by status and priority
- Input validation using FastAPI and Python typing (`Literal`)
- Relational database design with foreign key constraints
- Support for nullable relationships (e.g., unassigned issues)
- Automatic timestamp tracking (`created_at`, `updated_at`)
- SQL-based schema creation and data manipulation


## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** PostgreSQL
- **Database Access:** psycopg (SQL execution with cursor-based queries)
- **Language:** Python
- **API Testing:** Swagger UI (FastAPI auto-generated docs)
- **Version Control:** Git & GitHub

## API Endpoints

### Users

- `POST /users` — Create a new user  
- `GET /users` — Retrieve all users  
- `GET /users/{user_id}` — Retrieve a specific user  

### Issues

- `POST /issues` — Create a new issue  
- `GET /issues` — Retrieve all issues (supports filtering by status and priority)  
- `GET /issues/{issue_id}` — Retrieve a specific issue  
- `PUT /issues/{issue_id}` — Update an issue  
- `DELETE /issues/{issue_id}` — Delete an issue  

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/brienbledsoe/incident-tracking-api.git
cd incident-tracking-api
```

### 2. Create and activate a virtual enviornment

```bash
python -m venv venv
venv\Scripts\activate #on Windows
```

### 3. Install dependencies

```bash
pip install fastapi psycopg uvicorn
```

### 4. Set up PostgreSQL 

```bash
- Create a PosgreSQL database
- Run the SQL scripts in the SQL/ folder to create tables
```

### 5. Run the FastAPI server

```bash
uvicorn main:app --reload
```

### 6. Access the API 

```bash
- open your browser and go to: 
- http://127.0.0.1:8000/docs
- This will open the Swagger UI where you can test all endpoints
```