# Docker Installation Guide

## Prerequisites

Ensure you have Docker and Docker Compose installed on your system.

## Steps

1. **Clone the Repository**
   - Execute `git clone https://github.com/danlopatenco/product_price_monitor.git` to clone the project to your local machine.

2. **Run Docker Compose**
   - Navigate to the project directory.
   - Execute `docker-compose up` to build and start the containers.

3. **Access the Application**
   - The application will be accessible at `http://localhost:8000` once the containers are running.

Note: Docker Compose will handle the installation of dependencies, environment setup, and database migrations automatically.

## Execute Tests

Run `docker-compose exec app python manage.py test` test to execute the tests.
Here, web is the name of the Docker service running your Django application. Adjust this service name based on your docker-compose.yml configuration.