# Task Management App

This is a simple task management application built using Flask and following the 12-factor app methodology.

## Setup and Installation

Note: This repository should be under version control with Git. If you're starting a new project, initialize a Git repository before proceeding.

1. Clone the repository (or create and initialize a new one if starting from scratch):

   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

   If creating a new repository:

   ```
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Install Docker and Docker Compose if you haven't already.

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

For local development without Docker:

1. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   - Copy the `.env.example` file to `.env`
   - Update the values in `.env` as needed

4. Database Initialization:
   The application now automatically checks for the existence of required tables and creates them if they don't exist. This process occurs when the application starts, so you don't need to manually initialize the database.

## Running the Application

To run the application using Docker:

```
docker-compose up
```

To run the application locally without Docker:

```
flask run
```

For production deployment, use:

```
gunicorn app:app
```

## Running Tests

To run the unit tests:

```
pytest
```

## API Endpoints

- `GET /`: Welcome message
- `GET /tasks`: Get all tasks
- `POST /tasks`: Create a new task
- `PUT /tasks/<task_id>`: Update a task
- `DELETE /tasks/<task_id>`: Delete a task

## Error Handling

The application now includes proper error handling for common HTTP errors (400, 404, 500). Each error returns a JSON response with an error message.

## 12-Factor App Principles Applied

1. Codebase: The application is version-controlled using Git.
2. Dependencies: All dependencies are declared in requirements.txt.
3. Config: Configuration is stored in environment variables.
4. Backing Services: The database is treated as an attached resource.
5. Build, release, run: The build and run stages are separated using Docker.
6. Processes: The app runs as a stateless process.
7. Port binding: The app binds to a port and is accessible as a service.
8. Concurrency: The app can scale horizontally using Docker Swarm.
9. Disposability: The app can be started or stopped quickly.
10. Dev/prod parity: Development and production environments are kept as similar as possible using Docker.
11. Logs: The app writes logs to stdout.
12. Admin processes: Admin tasks can be run as one-off processes in the same environment as the app.

## Docker and Docker Swarm

This application is containerized using Docker and can be deployed using Docker Swarm for orchestration. The `Dockerfile` defines the application's container, while `docker-compose.yml` is used for local development and testing. For production deployment with Docker Swarm, use the `docker-stack.yml` file.

To deploy the application using Docker Swarm:

1. Initialize a Docker Swarm (if not already done):

   ```
   docker swarm init
   ```

2. Deploy the stack:

   ```
   docker stack deploy -c docker-stack.yml task-management-app
   ```

3. Scale the application as needed:

   ```
   docker service scale task-management-app_web=3
   ```

4. Remove the stack when done:

   ```
   docker stack rm task-management-app
   ```

5. Codebase: One codebase tracked in revision control (Git)
6. Dependencies: Explicitly declare and isolate dependencies (requirements.txt)
7. Config: Store config in the environment (.env file)
8. Backing services: Treat backing services as attached resources (SQLite database)
9. Build, release, run: Strictly separate build and run stages (Procfile)
10. Processes: Execute the app as one or more stateless processes
11. Port binding: Export services via port binding
12. Concurrency: Scale out via the process model (can be handled by Gunicorn)
13. Disposability: Maximize robustness with fast startup and graceful shutdown
14. Dev/prod parity: Keep development, staging, and production as similar as possible
15. Logs: Treat logs as event streams (using Python's logging module)
16. Admin processes: Run admin/management tasks as one-off processes (can be implemented as needed)
