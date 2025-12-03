# DatabaseProject

A full-stack web application built with Flask backend and React frontend for managing a university database system.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 14+** - [Download Node.js](https://nodejs.org/)
- **PostgreSQL 12+** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git** - [Download Git](https://git-scm.com/)

To verify your installations, run these commands in your terminal:

```bash
python --version
node --version
npm --version
psql --version
```

## Project Structure

```
DatabaseProject/
├── backend/                    # Flask backend server
│   ├── app.py                 # Main Flask application
│   ├── config.example.py      # Example configuration file
│   ├── requirements.txt       # Python dependencies
│   ├── setup_db.py            # Database setup script
│   └── routes/                # API route handlers
├── frontend/                   # React frontend application
│   ├── src/                   # React source files
│   ├── public/                # Static files
│   └── package.json           # Node dependencies
├── ERtoRelational.sql         # Database schema
├── Inserts.sql                # Sample data inserts
├── Queries.sql                # Database queries
└── README.md                  # This file
```

## Backend Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rgholdre/DatabaseProject.git
cd DatabaseProject
```

### 2. Create Python Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

### 4. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Configure Database Connection

1. Copy the example config file:
   ```bash
   cp config.example.py config.py
   ```

2. Edit `config.py` and add your PostgreSQL credentials:
   ```python
   DB_CONFIG = {
       "host": "localhost",
       "database": "DBProject",
       "user": "postgres",
       "password": "YOUR_PASSWORD",  # Replace with your PostgreSQL password
       "port": "5432"
   }
   ```

### 6. Set Up Database

1. Ensure PostgreSQL is running on your system

2. Create the database and tables:
   ```bash
   python setup_db.py
   ```

   This will:
   - Create the `DBProject` database (if it doesn't exist)
   - Run the schema from `ERtoRelational.sql`
   - Populate sample data from `Inserts.sql`

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd ../frontend
```

### 2. Install Node Dependencies

```bash
npm install
```

This will install all required packages from `package.json`.

## Running the Application

### Option 1: Run Both Servers Together

From the project root directory, run both servers in separate terminals:

**Terminal 1 - Backend Server:**
```bash
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python app.py
```

The backend will start on `http://127.0.0.1:5000`

**Terminal 2 - Frontend Server:**
```bash
cd frontend
npm start
```

The frontend will start on `http://localhost:3000`

### Option 2: Run Backend Only

If you only want to run the backend API:

```bash
cd backend
source .venv/bin/activate
python app.py
```

The API will be available at `http://127.0.0.1:5000`

### Option 3: Run Frontend Only

If you only want to run the frontend (make sure backend is running):

```bash
cd frontend
npm start
```

The frontend will be available at `http://localhost:3000`

## Backend Dependencies

The backend requires the following Python packages (in `requirements.txt`):

- **flask** - Web framework
- **flask-cors** - Handle Cross-Origin Resource Sharing
- **psycopg2-binary** - PostgreSQL adapter for Python
- **python-dotenv** - Load environment variables from .env files

## Frontend Dependencies

The frontend is a React application with the following key technologies:

- **React** - UI library
- **react-dom** - DOM rendering
- **axios** - HTTP client (if used)

## Troubleshooting

### Python Command Not Found
- **Issue**: `zsh: command not found: python`
- **Solution**: Use `python3` instead, or ensure Python is in your PATH

### Virtual Environment Not Activating
- **Issue**: Virtual environment won't activate
- **Solution**: Verify `.venv` folder exists and run the correct activation command for your OS

### PostgreSQL Connection Error
- **Issue**: `psycopg2.OperationalError: could not connect to server`
- **Solution**:
  - Ensure PostgreSQL is running
  - Check your database credentials in `config.py`
  - Verify the database `DBProject` exists

### npm audit vulnerabilities
- **Issue**: npm shows vulnerabilities after `npm install`
- **Solution**: Run `npm audit fix` to patch known vulnerabilities (optional for development)

### React Port Already in Use
- **Issue**: `Port 3000 is already in use`
- **Solution**: Kill the process using port 3000 or run on a different port:
  ```bash
  PORT=3001 npm start
  ```

### Flask Port Already in Use
- **Issue**: `Address already in use`
- **Solution**: Kill the process using port 5000 or modify `app.py` to use a different port

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes to the backend and/or frontend

3. Test your changes locally

4. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

5. Create a pull request on GitHub

## API Documentation

For API endpoints and documentation, refer to `backend/routes/` directory and Flask route definitions in `app.py`.

## Database Schema

The database schema is defined in `ERtoRelational.sql`. To view the schema:

```bash
psql -U postgres -d DBProject -f ERtoRelational.sql
```

## Support

For issues or questions, please open an issue on the GitHub repository or contact the project maintainers.

