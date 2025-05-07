# Part B: Architecture & Design Document

**Candidate:** Huynh  
**Role:** Software Developer
**Stack:** Django + DRF + Docker + GitHub Actions + SQLite

---

## 1. High-Level Architecture Diagram

![Architecture Diagram](zinc_architecture_diagram.png)

- The user triggers ingestion from a CSV file.
- Django reads the CSV and stores data in SQLite.
- APIs expose aggregated metrics.
- CI/CD ensures code quality and builds Docker images automatically.

---

## 2. API & Data Model Sketch

### APIs

| Endpoint                     | Method | Description                         |
|------------------------------|--------|-------------------------------------|
| `/api/import-sales/`         | GET    | Ingest sales from `sales.csv`       |
| `/api/metrics/revenue/`      | GET    | Total and average revenue           |
| `/api/metrics/revenue/daily/`| GET    | Daily revenue grouped by date       |
| `/api/health/`               | GET    | Health check (DB connectivity)      |

### Data Model

```python
class Sale(models.Model):
    date = models.DateField()
    order_id = models.CharField(max_length=50)
    product_id = models.CharField(max_length=100)
    amount_sgd = models.FloatField()
```

---

## 3. Infrastructure Choices

| Component         | Choice           | Justification                                   |
|-------------------|------------------|-------------------------------------------------|
| Web Framework     | Django + DRF     | Rapid development, ORM, API handling            |
| DB                | SQLite           | Lightweight for assignment, easy to run         |
| Containerization  | Docker           | Reproducible builds, portable                   |
| WSGI Server       | Gunicorn         | Production-grade                                |
| CI/CD             | GitHub Actions   | Automated test/build                            |
| Logging           | python-json-logger + middleware | Structured logs with `request_id`|

---

## 4. Scaling & Resilience Strategy

- Replace SQLite with PostgreSQL for concurrent writes and volume.
- Add Redis caching for frequent metrics queries.
- Enable pagination and filtering for endpoints.
- Deploy to AWS ECS/Fargate or GCP Cloud Run with Docker image.

---

## 5. CI/CD & Rollback Plan

- GitHub Actions triggers on push to `main`.
- Runs migrations, unit tests, and Docker build.
- CI validates correctness before deploy.
- In production: tag and version Docker images; rollback = redeploy prior tag.

---

## 6. Observability & SRE

- All API logs are structured JSON with timestamp, request_id, endpoint, params.
- `RequestIDMiddleware` injects UUID into each request.
- Health endpoint verifies DB access.
- Logs flow through stdout (Docker-compatible).

---

## 7. Trade-Off Discussion

| Area           | Decision                          | Trade-Off                 |
|----------------|-----------------------------------|---------------------------|
| DB             | SQLite for simplicity             | Not scalable for prod     |
| CSV Source     | Local file                        | No file upload API        |
| API View       | DRF APIView over function views   | Slightly more verbose     |
| Dockerfile     | Multi-stage                       | Small image size          |
| CI             | GitHub Actions only               | No deploy, just build/test|
| Logging        | Custom middleware                 | More setup, more control  |

