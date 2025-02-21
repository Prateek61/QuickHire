# Backend

This is the backend of the project. It is a FastAPI application that provides a REST API to the frontend.

## Run Locally

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

```bash
source .venv/bin/activate
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Create database tables

```bash
python scripes/create_tables.py
```

### Run the application

```bash
fastapi dev app
```