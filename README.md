# Secure Manage App

![CI](https://github.com/museteka01/secure-manage-app/actions/workflows/ci.yml/badge.svg)

A secure user-management API built with **FastAPI** and **PostgreSQL**, packaged with
**Docker**, tested and security-scanned in **GitHub Actions**, and deployable to
**AWS ECS Fargate**, with supporting infrastructure in **Terraform**.

## The problem it solves

Small teams often ship internal APIs with hard-coded admin logins, secrets in source
code and no automated checks. A single leaked repo then exposes every environment.
This project shows the opposite: real password hashing, short-lived JWTs, secrets
kept out of git, a non-root container, and a pipeline that blocks bad code and
vulnerable dependencies before they ship.

## Features

- User registration and login with **bcrypt** password hashing
- **JWT** bearer tokens (PyJWT) with expiry
- Protected endpoints (`/api/v1/users/me`, `/api/v1/users/`)
- Input validation (username format, minimum password length)
- Liveness (`/health`) and database readiness (`/health/db`, returns 503 when down)
- All secrets loaded from environment variables - none in the code
- Docker image runs as a **non-root** user with a built-in health check
- CI: flake8 lint, **bandit** code scan, **pip-audit** dependency CVE scan, pytest, Docker build
- Manual, one-click deploy to **AWS ECR + ECS Fargate**, secrets pulled from **SSM Parameter Store**
- Terraform for a private, versioned, encrypted S3 bucket

## Tech stack

Python 3.12 | FastAPI | SQLAlchemy 2 | PostgreSQL 16 | Docker / Compose |
GitHub Actions | AWS (ECR, ECS Fargate, SSM, CloudWatch Logs, S3) | Terraform

## Project structure

    secure-manage-app/
    |-- app/
    |   |-- main.py            # FastAPI app, routers, table creation on startup
    |   |-- schemas.py         # Pydantic request/response models
    |   |-- core/
    |   |   |-- config.py      # settings from environment / .env
    |   |   |-- security.py    # bcrypt hashing, JWT create/verify
    |   |   `-- deps.py        # get_current_user dependency
    |   |-- db/
    |   |   |-- session.py     # engine, SessionLocal, Base (single source)
    |   |   `-- deps.py        # get_db dependency
    |   |-- models/user.py     # User table
    |   `-- routers/           # health, auth, users
    |-- tests/                 # pytest suite (runs on SQLite, no DB needed)
    |-- deploy/task-definition.json
    |-- terraform/
    |-- .github/workflows/     # ci.yml, aws-deploy.yml
    |-- Dockerfile
    |-- docker-compose.yml
    |-- requirements.txt / requirements-dev.txt
    `-- .env.example

## Run it locally with Docker

    cp .env.example .env
    # edit .env: set SECRET_KEY and POSTGRES_PASSWORD (and match DATABASE_URL)
    docker compose up --build

Open http://localhost:8000/docs for the interactive API.

## Run it without Docker (development)

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements-dev.txt
    cp .env.example .env          # then edit it
    uvicorn app.main:app --reload

## Run the tests

    pytest -v

## API quick tour

    # register
    curl -X POST localhost:8000/api/v1/auth/register \
      -H "Content-Type: application/json" \
      -d '{"username":"alice","password":"S3cure-pass!"}'

    # log in (returns an access token)
    curl -X POST localhost:8000/api/v1/auth/login \
      -d "username=alice&password=S3cure-pass!"

    # call a protected endpoint
    curl localhost:8000/api/v1/users/me -H "Authorization: Bearer <token>"

## Deploying to AWS

1. Create an ECR repository `secure-manage-app`, an ECS cluster `secure-manage-cluster`
   and a Fargate service `secure-manage-service`.
2. Store `SECRET_KEY` and `DATABASE_URL` as SecureString parameters under
   `/secure-manage/` in SSM Parameter Store.
3. Fill in the `<AWS_ACCOUNT_ID>` and `<AWS_REGION>` placeholders in
   `deploy/task-definition.json`.
4. Add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_REGION` as GitHub
   repository secrets.
5. Actions tab -> **Deploy to AWS ECS** -> **Run workflow**.

## Security controls and the standards they support

| Control | Supports |
|---|---|
| bcrypt password hashing, no hard-coded credentials | OWASP Top 10 A02/A07, NIST 800-53 IA-5 |
| Secrets in env / SSM, never in git | OWASP A05, NIST 800-53 SC-28, ISO 27001 A.8.24 |
| Uniform login errors, token expiry | OWASP A07, NIST 800-53 AC-7 / IA-11 |
| Input validation with Pydantic | OWASP A03 |
| bandit + pip-audit in CI | OWASP A06, NIST SSDF, ISO 27001 A.8.28 |
| Non-root container, private DB network | CIS Docker Benchmark 4.1, NIST 800-53 AC-6 |
| Encrypted, versioned, non-public S3 | NIST 800-53 SC-28 / CP-9, ISO 27001 A.8.13 |

## Roadmap

- Alembic database migrations
- Role-based access control (admin vs user)
- Rate limiting on the login endpoint
- GitHub OIDC to AWS instead of long-lived access keys
- Terraform for the full ECS / RDS stack
