# House Hive API

Backend API for the House Hive application. It provides authentication,
house management, house membership, chores, events, and token revocation
support using FastAPI, PostgreSQL, SQLAlchemy, Alembic, and JWT auth.

## Requirements

- Python 3.14+
- PostgreSQL
- uv

## Setup

Install dependencies:
```bash
uv sync
```

Create a local env file:
```bash
cp .env.example .env
```

Generate a JWT secret and put it in `.env`:
```bash
openssl rand -hex 32
```

Required env values:
```env
APP_NAME=HouseHive
ENVIRONMENT=development
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8000","http://127.0.0.1:3000","http://127.0.0.1:8000"]

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=house_hive

JWT_SECRET_KEY=<long-random-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
```

## Database

Create the database if needed:
```bash
createdb house_hive
```

Run migrations:
```bash
uv run alembic upgrade head
```

Create a migration after model changes:
```bash
uv run alembic revision --autogenerate -m "describe change"
```

## Run

```bash
uv run fastapi dev app/main.py
```

The API is served at `http://localhost:8000`. Interactive docs are available at
`http://localhost:8000/docs`.

## Auth

Register a user:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "exampleuser",
    "first_name": "Example",
    "last_name": "User",
    "password": "password123456"
  }'
```

Login with an email or username:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123456"
```

Use an access token:
```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <jwt-token>"
```

Swagger authorization uses `POST /api/v1/auth/token`, which returns a top-level
OAuth-compatible token response.

## Endpoints

Auth:
```text
POST /api/v1/auth/register      Create a regular user and return token pair
POST /api/v1/auth/login         Return the user and token pair
POST /api/v1/auth/token         Swagger/OAuth-compatible token endpoint
POST /api/v1/auth/refresh       Return a new access token from a refresh token
POST /api/v1/auth/logout        Revoke the presented access or refresh token
GET  /api/v1/auth/me            Return the current user
GET  /api/v1/auth/admin-only    Require an admin user
```

Houses:
```text
POST   /api/v1/houses                 Create a house and assign creator as admin
GET    /api/v1/houses                 List houses for the current user
GET    /api/v1/houses/{house_id}      Read a house for a member
PATCH  /api/v1/houses/{house_id}      Update a house as admin
DELETE /api/v1/houses/{house_id}      Delete a house as admin
POST   /api/v1/houses/{house_id}/join Join a house as a member
```

House members:
```text
POST   /api/v1/house-members                  Add a user to a house as admin
GET    /api/v1/house-members?house_id=<uuid>  List house users and their roles
GET    /api/v1/house-members/{member_id}      Read a membership
PATCH  /api/v1/house-members/{member_id}      Update a member role as admin
DELETE /api/v1/house-members/{member_id}      Remove a membership
```

## Data Model

Core models:

- `User`: registered users and global app role.
- `House`: home profile with name, address, and room count.
- `HouseMember`: connection between users and houses, with `admin` or `member`
  role inside that house.
- `Event`: scheduled house event created by a house member.
- `Chore`: house task created by a user.
- `ChoreCompletion`: records a user completing a chore.
- `TokenBlocklist`: revoked access or refresh tokens.

## Quality

Run Ruff:
```bash
uv run ruff check .
```

Compile check:
```bash
uv run python -m compileall app
```

## Key Files

```text
app/main.py                         FastAPI app
app/api/router.py                   API router registration
app/api/v1/auth.py                  Auth routes
app/api/v1/house.py                 House routes
app/api/v1/house_member.py          House member routes
app/api/v1/schemas/                 Pydantic request/response schemas
app/api/v1/utils/house_member.py    House membership lookup/permission helpers
app/core/security.py                Password hashing and JWT logic
app/core/settings.py                Env settings
app/db/models/                      SQLAlchemy models
alembic/versions/                   DB migrations
```
