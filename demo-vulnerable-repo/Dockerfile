# Insecure Dockerfile for Demo
FROM python:3.8-slim

# Copy files
WORKDIR /app
COPY . /app

# Run pip installs
RUN pip install --no-cache-dir -r requirements.txt

# Expose server port
EXPOSE 5000

# Runs as root user by default (No USER directive specified)
CMD ["python", "src/app.py"]
