FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Create a non-root user
RUN adduser --disabled-password appuser
USER appuser

# Copy source and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 8000 and run Gunicorn
EXPOSE 8000
CMD ["gunicorn", "zinc_project.wsgi:application", "--bind", "0.0.0.0:8000"]