
# Heroku Sample Application

This is a sample Flask application deployed on Heroku, which demonstrates the use of Auth0 for authentication and API management for movies and actors. The application includes several RESTful endpoints for managing movies and actors, and implements role-based access control (RBAC) with JWT tokens for secure access to protected resources. As database postgres PaaS in heroku is used. For testing purposes, local db is used.

## Project Structure

- **app.py**: The main Flask application file that defines the API endpoints and handles requests.
- **auth.py**: Handles authorization and token validation using Auth0.
- **models.py**: Contains the SQLAlchemy models for `Movie` and `Actor`, and handles database setup.
- **requirements.txt**: Lists the Python dependencies required by the application.
- **test-app.py**: Unit tests for the API endpoints.
- **setup.sh**: Setting-up OS environment variables
- **runtime.txt**: decribes environment used by Heroku

## Installation

To run this project locally, follow the steps below:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the project directory**:
   ```bash
   cd heroku_sample
   ```

3. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   Run setup.sh for setting-up following environment variables required for the Auth0 authentication:
   ```bash
   export AUTH0_DOMAIN='your-auth0-domain'
   export ALGORITHMS=['RS256']
   export API_AUDIENCE='your-api-audience'
   export DATABASE_URL='database-url'
   ```

  


6. **Run the application**:
   ```bash
   export FLASK_APP=app.py
   flask run
   ```

## Authorization

The application uses Auth0 for authentication and authorization. JWT tokens are required to access most of the API endpoints. Users are assigned roles that grant them specific permissions to create, update, delete, or view movies and actors.

- **Roles**:
  - **Casting Assistant**:
    - Can view actors and movies
  - **Casting Director**:
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
  - **Executive Producer**:
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database



To access a protected endpoint, include a valid JWT token in the `Authorization` header:

```bash
Authorization: Bearer <your-jwt-token>
```
Valid tokens for testing purposes are stored in test-app.py

## API Endpoints

### Movies Endpoints

- **GET /movies**
  - Description: Fetches a list of all movies.
  - Permissions: `read:all`
  - Example Request:
    ```bash
    curl -X GET http://localhost:5000/movies -H "Authorization: Bearer <your-jwt-token>"
    ```

- **POST /movies**
  - Description: Creates a new movie.
  - Permissions: `create-delete:movie`
  - Example Request:
    ```bash
    curl -X POST http://localhost:5000/movies -H "Authorization: Bearer <your-jwt-token>" \
         -H "Content-Type: application/json" \
         -d '{"title": "New Movie", "release_date": "2024-01-01", "actors": [1, 2]}'
    ```

- **PATCH /movies/<int:movie_id>**
  - Description: Updates an existing movie.
  - Permissions: `update:all`
  - Example Request:
    ```bash
    curl -X PATCH http://localhost:5000/movies/1 -H "Authorization: Bearer <your-jwt-token>" \
         -H "Content-Type: application/json" \
         -d '{"title": "Updated Movie Title", "release_date": "2025-01-01"}'
    ```

- **DELETE /movies/<int:movie_id>**
  - Description: Deletes a movie by ID.
  - Permissions: `create-delete:movie`
  - Example Request:
    ```bash
    curl -X DELETE http://localhost:5000/movies/1 -H "Authorization: Bearer <your-jwt-token>"
    ```

### Actors Endpoints

- **GET /actors**
  - Description: Fetches a list of all actors.
  - Permissions: `read:all`
  - Example Request:
    ```bash
    curl -X GET http://localhost:5000/actors -H "Authorization: Bearer <your-jwt-token>"
    ```

- **POST /actors**
  - Description: Creates a new actor.
  - Permissions: `create-delete:actor`
  - Example Request:
    ```bash
    curl -X POST http://localhost:5000/actors -H "Authorization: Bearer <your-jwt-token>" \
         -H "Content-Type: application/json" \
         -d '{"name": "New Actor", "age": 30, "gender": "male"}'
    ```

- **PATCH /actors/<int:actor_id>**
  - Description: Updates an existing actor.
  - Permissions: `update:all`
  - Example Request:
    ```bash
    curl -X PATCH http://localhost:5000/actors/1 -H "Authorization: Bearer <your-jwt-token>" \
         -H "Content-Type: application/json" \
         -d '{"name": "Updated Actor Name", "age": 35}'
    ```

- **DELETE /actors/<int:actor_id>**
  - Description: Deletes an actor by ID.
  - Permissions: `create-delete:actor`
  - Example Request:
    ```bash
    curl -X DELETE http://localhost:5000/actors/1 -H "Authorization: Bearer <your-jwt-token>"
    ```

## Running Tests

To run the unit tests, use the following command:

```bash
python -m unittest discover
```

