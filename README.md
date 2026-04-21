# Insurance Advisor Backend

A production-ready FastAPI backend for the Insurance Advisor application.

## Features
- **Clean Architecture**: Organized into models, schemas, routes, database, and utils.
- **Authentication**: JWT-based authentication with bcrypt password hashing.
- **Database**: PostgreSQL integration with SQLAlchemy ORM.
- **Security**: Environment variable configuration and CORS middleware.
- **Validation**: Pydantic models for request/response validation.

## Prerequisites
- Python 3.8+
- PostgreSQL server

## Installation

1. **Clone the repository** (if applicable) and navigate to the project directory.

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # source venv/bin/activate    # On Unix/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Edit the `.env` file and update your PostgreSQL credentials:
   ```env
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/insurance_advisor
   SECRET_KEY=your_random_secret_key
   ```
   *Note: Ensure the database `insurance_advisor` exists in your PostgreSQL.*

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`
Documentation: `http://127.0.0.1:8000/docs`

## API Endpoints

### Authentication
- `POST /register`: Create a new account.
- `POST /login`: Authenticate and receive a JWT token.

### Contact
- `POST /contact`: Submit a contact message.

---

## Example Requests

### 1. Register User
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/register' \
  -H 'Content-Type: application/json' \
  -d '{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}'
```

### 2. Login
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/login' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "john@example.com",
  "password": "securepassword123"
}'
```

### 3. Contact Message
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/contact' \
  -H 'Content-Type: application/json' \
  -d '{
  "full_name": "Jane Smith",
  "email": "jane@example.com",
  "subject": "Insurance Inquiry",
  "message": "I would like to know more about health insurance plans."
}'
```
