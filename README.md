# GIS Monitoring API

Backend service for monitoring geospatial objects and GSM meter measurements.

The project demonstrates a production-oriented Python backend architecture with authentication, authorization, PostgreSQL persistence, database migrations, automated tests and CI.

## Features

* User registration
* JWT authentication
* Protected API endpoints
* Monitoring object CRUD
* Per-user access control
* Measurement history
* Measurement filtering by date
* Measurement statistics
* PostgreSQL persistence
* SQLAlchemy ORM
* Alembic migrations
* Automated API tests
* GitHub Actions CI

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* JWT
* Pytest
* GitHub Actions

## Project Structure

```text
app/
├── main.py
├── config.py
├── database.py
├── security.py
├── schemas.py
│
├── models/
│   ├── user.py
│   ├── monitoring_object.py
│   └── measurement.py
│
├── repositories/
│   ├── users.py
│   ├── monitoring_objects.py
│   └── measurements.py
│
└── routers/
    ├── auth.py
    ├── monitoring_objects.py
    └── measurements.py

migrations/
tests/
.github/workflows/
```

## Architecture

The application is separated into several layers:

```text
HTTP Request
    ↓
FastAPI Router
    ↓
Pydantic Validation
    ↓
Repository Layer
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

Authentication is handled using JWT access tokens.

Monitoring objects belong to individual users, so authenticated users can only access their own objects and measurement data.

## API

### Authentication

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

### Monitoring Objects

```text
POST   /monitoring-objects
GET    /monitoring-objects
GET    /monitoring-objects/{id}
PATCH  /monitoring-objects/{id}
DELETE /monitoring-objects/{id}
```

### Measurements

```text
POST /monitoring-objects/{id}/measurements

GET /monitoring-objects/{id}/measurements

GET /monitoring-objects/{id}/measurements/statistics
```

Measurement history can be filtered using date parameters.

## Example

Create a monitoring object:

```json
{
  "name": "GSM Meter 001",
  "latitude": 59.3293,
  "longitude": 18.0686
}
```

Example response:

```json
{
  "id": 1,
  "name": "GSM Meter 001",
  "latitude": 59.3293,
  "longitude": 18.0686
}
```

Add a measurement:

```json
{
  "value": 15342.7
}
```

## Local Installation

Clone the repository:

```bash
git clone https://github.com/TrippleT25/diplom-gis-monitoring.git
cd diplom-gis-monitoring
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/gis_monitoring

SECRET_KEY=your-secret-key

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit `.env` to the repository.

## Database

Create the PostgreSQL database:

```sql
CREATE DATABASE gis_monitoring;
```

Apply migrations:

```bash
alembic upgrade head
```

## Run

Start the application:

```bash
python -m uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Tests

Create a separate PostgreSQL database:

```sql
CREATE DATABASE gis_monitoring_test;
```

Create `.env.test`:

```env
TEST_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/gis_monitoring_test
```

Run the test suite:

```bash
pytest -v
```

The tests cover:

* health check
* authentication requirements
* monitoring object creation
* object retrieval
* object updates
* object deletion
* input validation

## CI

The repository uses GitHub Actions.

Tests are automatically executed on:

```text
push
pull_request
```

The CI environment starts a PostgreSQL service and executes the test suite automatically.

## Security

Passwords are never stored in plain text.

The application stores password hashes and uses JWT access tokens for authentication.

Monitoring objects are associated with their owners, preventing authenticated users from accessing another user's objects through the API.

## Development Status

The project is under active development.

Planned improvements:

* pagination
* advanced filtering
* API logging
* role-based access control
* PostGIS integration
* improved test coverage
* deployment
