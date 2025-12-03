# Complaint / Helpdesk Management System

A full-stack Complaint / Helpdesk / Ticket Management System built with a Flask backend and a React (Vite) frontend.
The system supports three roles: **User**, **Agent**, and **Admin**, each with separate privileges and workflows.

## Features

### Authentication & Authorization

- Secure JWT-based login and registration
- Role-based access: User, Agent, Admin

### Ticket Management

- Create, edit, and track tickets
- Upload multiple images per ticket
- Add and view comments on tickets
- Ticket workflow: Open → In-Progress → Resolved

### Dashboards

- User dashboard (personal tickets)
- Agent dashboard (assigned tickets)
- Admin dashboard (complete system visibility)

### Ticket Detail View

- Image gallery
- Comment timeline
- Status and metadata display

## Project Structure

```
.
├── backend
│   ├── app.py
│   ├── data.db
│   ├── insert_dummy_data.py
│   ├── models.py
│   ├── openapi.yml
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── setup_db.py
│   ├── tests
│   └── venv
├── frontend
│   ├── index.html
│   ├── package.json
│   ├── public
│   └── src
└── README.md
```

## Technologies Used

### Backend

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- PyJWT
- python-dotenv

### Frontend

- React
- Vite
- React Router

## Setup and Installation

### Prerequisites

- Python 3.x
- Node.js and npm

## Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/kavyansh-bagdi/helpdesk-management.git
   cd helpdesk-management/backend
   ```

2. Create and activate the virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:

   ```bash
   python setup_db.py
   python insert_dummy_data.py
   ```

## Frontend Setup

1. Navigate to the frontend folder:

   ```bash
   cd ../frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

## Running the Application

### Start the backend server:

```bash
cd backend
flask run
```

Backend runs at: `http://127.0.0.1:5000`

### Start the frontend development server:

```bash
cd frontend
npm run dev
```

Frontend runs at: `http://localhost:5173`

## API Documentation

The complete API specification is available in:

```
backend/openapi.yml
```

You can import it into tools like Postman or Swagger UI.

## Running Tests

Backend unit tests are written using Pytest.

Run all tests:

```bash
cd backend
pytest
```
