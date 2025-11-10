# Complaint / Helpdesk Management

This is a full-stack Complaint / Helpdesk Management application with a Flask backend and a React frontend.

## Features

- User registration and login
- Create, view, and update support tickets with multiple image uploads
- A dashboard to view all tickets
- A detail view for each ticket with image gallery

## Technologies Used

### Backend

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

### Frontend

- [React](https://reactjs.org/)
- [Vite](https://vitejs.dev/)
- [React Router](https://reactrouter.com/)

## Setup and Installation

### Prerequisites

- Python 3.x
- Node.js and npm

### Backend Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/kavyansh-bagdi/helpdesk-management.git
    cd helpdesk-management/backend
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the database:**

    ```bash
    python setup_db.py
    python insert_dummy_data.py
    ```

### Frontend Setup

1.  **Navigate to the frontend directory:**

    ```bash
    cd ../frontend
    ```

2.  **Install the dependencies:**

    ```bash
    npm install
    ```

## Running the Application

1.  **Start the backend server:**

    ```bash
    cd ../backend
    flask run
    ```

    The backend will be running at `http://127.0.0.1:5000`.

2.  **Start the frontend development server:**

    ```bash
    cd ../frontend
    npm run dev
    ```

    The frontend will be running at `http://localhost:5173`.

## API Documentation

The API is documented using OpenAPI. The documentation can be found in the `openapi.yml` file.
