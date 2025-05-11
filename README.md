# Benchmark Project README

## Overview

This is a fitness tracking application called Benchmark, designed to help users monitor their exercise routines and dietary habits. The application allows users to log their food intake, track their workouts, set fitness goals, and analyze their progress over time.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose

## Getting Started

Follow these steps to launch the application:

1. Clone the repository to your local machine.

   ```
   git clone https://github.com/isaiahrivera21/BenchMark
   cd BenchMark
   ```

2. Build and start the Docker containers.

   ```docker compose up --build```

   This command will create and start the necessary containers for the application.

3. In a new terminal tab, execute the following command to access the web container's shell:

   ```docker exec -it benchmark-web-1 bash```

4. Once inside the container, run the following commands to set up the database and populate it with initial data:

    ```
    poetry run python manage.py migrate
   poetry run python manage.py populatefood
   poetry run python manage.py populateexercise
   ```

   These commands will apply database migrations and populate the database with food and exercise data.

5. Start the Django development server:

   ```poetry run python manage.py runserver 0.0.0.0:8000```

   This will start the server and make the application accessible at http://localhost:8000.

## Accessing the Application

Once the server is running, open your web browser and navigate to http://localhost:8000 to access the Benchmark application.
