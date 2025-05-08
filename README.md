*** Zinc Take-Home Assignment

##This project is built with Django + DRF, using Docker for containerization and GitHub Actions for CI. It includes sales ingestion from CSV, revenue metrics APIs, structured logging, health checks, and unit tests.
--------------------------------------------------------
I - Run Locally (without Docker)
	1.	Clone the repo and install dependencies:
            git clone https://github.com/YOUR_USERNAME/zinc-assignment.git
            cd zinc-assignment
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
	2.	Run migrations and start the server:
            python manage.py migrate
            python manage.py runserver
	3.	Access the API:

            •	Import sales: http://localhost:8000/api/import-sales/
            •	Revenue: http://localhost:8000/api/metrics/revenue/?start=2025-03-01&end=2025-04-01
            •	Health check: http://localhost:8000/api/health/

-------------------------------------------

II - Run with Docker
	1.	Build Docker image:
            docker build -t zinc-app .
	2.	Run the container:
            docker run -p 8000:8000 zinc-app

-------------------------------------------
Test on: http://localhost:8000/
Locally:
python manage.py test


III - API Endpoints Summary

    GET  /api/import-sales/              -> Import sales from CSV
    GET  /api/metrics/revenue/           -> Total & average revenue
    GET  /api/metrics/revenue/daily/     -> Daily revenue breakdown
    GET  /api/health/                    -> Health check

IV - Tech Stack
	•	Python 3.10
	•	Django + DRF
	•	SQLite (for simplicity)
	•	Docker
	•	Gunicorn
	•	GitHub Actions CI
	•	Structured Logging (python-json-logger)
