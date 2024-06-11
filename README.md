# Social Network API

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Shyam2615/Social-Network-Api.git
    cd social_network
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

7. **Access the API** at `http://localhost:8000/api/`.

## API Endpoints

- `POST /api/signup/` - User Signup
- `POST /api/login/` - User Login
- `GET /api/token/refresh/` - Refresh Access Token
- `GET /api/search/?search=<keyword>` - User Search
- `POST /api/friend-request/<int:user_id>/` - Send Friend Request
- `POST /api/friend-request/<int:request_id>/<str:action>/` - Accept/Reject Friend Request
- `GET /api/friends/` - List Friends
- `GET /api/friend-requests/` - List Pending Friend Requests

## Running with Docker

1. **Build and start the Docker containers**:

    ```bash
    docker-compose up --build
    ```

2. **Apply migrations**:

    ```bash
    docker-compose run web python manage.py migrate
    ```

3. **Create a superuser**:

    ```bash
    docker-compose run web python manage.py createsuperuser
    ```

4. **Access the API** at `http://localhost:8000/api/`.
