# Loans For Good - Backend

## Summary
- [Demo](#demo)
- [How to Build the project](#how-to-build-the-project)
- [Project explanation](#project-explanation)
- [EAV explanation](#eav-explanation)
- [Test Coverage](#test-coverage)

## Demo

## How to build the project
To build the project, you have to download this repo and the [frontend](https://github.com/jsobralgitpush/lfg_frontend_redux) one. After that, create an app tree like this
```
(root)
├── loans_for_good_backend
│   ├── (this repo)
├── loans_for_good_frontend
└── docker-compose.yml
```
and use this `docker-compose.yml`, setting the following `config-vars` as your preference or use the current ones from the example (just to test the app)
- env
```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DEBUG=
DATABASE_URL=
REACT_APP_API_HOSTNAME=
```
- docker-compose.yml
```
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword

  backend:
    build:
      context: ./loans_for_good_backend
    command: ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    volumes:
      - ./loans_for_good_backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DEBUG: 'True'
      DATABASE_URL: postgresql://myuser:mypassword@db:5432/mydatabase

  frontend:
    build:
      context: ./loans_for_good_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./loans_for_good_frontend:/app
    environment:
      REACT_APP_API_HOSTNAME: http://localhost:8000
  
  redis:
    image: "redis:latest"
    ports:
      - "6379:6379"

  celery:
    build:
      context: ./loans_for_good_backend
    command: celery -A loans_for_good worker --loglevel=info
    volumes:
      - ./loans_for_good_backend:/app
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://myuser:mypassword@db:5432/mydatabase

volumes:
  postgres_data:

```

## Project explanation

## EAV explanation

## Test Coverage
