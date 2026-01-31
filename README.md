# Bank App

## Author

- **Name:** Vera Kibin
- **Group:** 2

---

## Prerequisites

Before starting, ensure you have the following installed:

- Python 3.10+
- pip (Python package manager)
- Docker + Docker Compose (for MongoDB)
- (Optional) curl (for quick sanity checks)

---

## How to Start the App

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **(Optional) Start MongoDB via Docker**
   If you want to run the API with persistence (as in CI):

   ```bash
   docker compose -f mongo.yml up -d
   ```

   Verify MongoDB is running:

   ```bash
   docker ps
   ```

3. **Run the Flask API Server**
   Open a new terminal and execute:

   ```bash
   export FLASK_APP=app/api.py
   export FLASK_ENV=development
   export PYTHONPATH=$PWD
   flask run
   ```

   The default address is: [http://127.0.0.1:5000](http://127.0.0.1:5000)

   > **Note:** If you use a different host/port, set the `BASE_URL` in your tests, e.g.:
   >
   > ```bash
   > export BASE_URL=http://127.0.0.1:5000
   > ```

---

## How to Execute Tests

### Unit Tests (with Coverage)

Run all unit tests with coverage:

```bash
python -m coverage run --source=src -m pytest tests/unit
python -m coverage report -m
```

(Optional) Generate an HTML coverage report:

```bash
python -m coverage html
```

### API Tests

A running Flask server is required (see "Run the Flask API Server" section). For tests with persistence, ensure MongoDB is running:

1. **Start MongoDB** (optional):

   ```bash
   docker compose -f mongo.yml up -d
   ```

2. **Start the API Server**:

   ```bash
   export FLASK_APP=app/api.py
   export FLASK_ENV=development
   export PYTHONPATH=$PWD
   flask run
   ```

3. **Run API Tests**:
   ```bash
   python -m pytest tests/api
   ```

### Performance Tests

A running Flask server is required (as above):

```bash
python -m pytest tests/perf
```

### BDD Tests (Behave)

To execute Gherkin scenarios:

```bash
behave
```

---

## Continuous Integration (CI)

The repository workflows include:

- Linting + Unit Tests (with 100% coverage gate)
- API Tests (with MongoDB and a running server)
- Performance Tests (with a running server)
