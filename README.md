# 💰 Expense Tracker API

A RESTful API built with Django REST Framework for managing personal financial transactions. Track your income and expenses with user authentication and secure JWT-based authorization.

## ✨ Features

-   🔐 **User Authentication** - Secure registration and JWT-based login
-   💸 **Transaction Management** - Create, read, update, and delete transactions
-   📊 **Transaction Types** - Support for both CREDIT (income) and DEBIT (expenses)
-   👤 **User-Specific Data** - Each user can only access their own transactions
-   🔒 **Protected Endpoints** - JWT authentication ensures data privacy
-   🐳 **Docker Support** - Easy deployment with Docker containerization

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

-   Python 3.12 or higher
-   pip (Python package manager)
-   Docker (optional, for containerized deployment)

### Installation

#### Option 1: Local Setup

1. **Clone the repository**

    ```bash
    git clone <your-repository-url>
    cd drf_basic
    ```

2. **Create a virtual environment**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser (optional)**

    ```bash
    python manage.py createsuperuser
    ```

6. **Start the development server**
    ```bash
    python manage.py runserver
    ```

The API will be available at `http://localhost:8000/`

#### Option 2: Docker Setup

1. **Build the Docker image**

    ```bash
    docker build -t expense-tracker .
    ```

2. **Run the container**
    ```bash
    docker run -p 8000:8000 expense-tracker
    ```

The API will be available at `http://localhost:8000/`

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api/
```

### Authentication Endpoints

#### Register a New User

```http
POST /api/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**

```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
}
```

#### Login

```http
POST /api/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response:**

```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Transaction Endpoints

> **Note:** All transaction endpoints require authentication. Include the JWT token in the Authorization header:
>
> ```
> Authorization: Bearer <your_access_token>
> ```

#### Get All Transactions

```http
GET /api/transactions/
Authorization: Bearer <your_access_token>
```

**Response:**

```json
{
    "data": [
        {
            "id": 1,
            "title": "Salary",
            "amount": 5000.0,
            "transaction_type": "CREDIT",
            "user_id": 1
        },
        {
            "id": 2,
            "title": "Grocery Shopping",
            "amount": -150.0,
            "transaction_type": "DEBIT",
            "user_id": 1
        }
    ]
}
```

#### Create a Transaction

```http
POST /api/transactions/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "title": "Freelance Project",
  "amount": 1500,
  "transaction_type": "CREDIT"
}
```

**Response:**

```json
{
    "message": "Transaction created successfully",
    "data": {
        "id": 3,
        "title": "Freelance Project",
        "amount": 1500.0,
        "transaction_type": "CREDIT",
        "user_id": 1
    }
}
```

#### Get a Specific Transaction

```http
GET /api/transactions/{id}/
Authorization: Bearer <your_access_token>
```

**Response:**

```json
{
    "data": {
        "id": 1,
        "title": "Salary",
        "amount": 5000.0,
        "transaction_type": "CREDIT",
        "user_id": 1
    }
}
```

#### Update a Transaction (Partial)

```http
PATCH /api/transactions/{id}/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "title": "Monthly Salary - Updated"
}
```

**Response:**

```json
{
    "message": "Transaction updated successfully",
    "data": {
        "id": 1,
        "title": "Monthly Salary - Updated",
        "amount": 5000.0,
        "transaction_type": "CREDIT",
        "user_id": 1
    }
}
```

#### Update a Transaction (Full)

```http
PUT /api/transactions/{id}/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "title": "Updated Transaction",
  "amount": 2000,
  "transaction_type": "CREDIT"
}
```

#### Delete a Transaction

```http
DELETE /api/transactions/{id}/
Authorization: Bearer <your_access_token>
```

**Response:**

```json
{
    "message": "Transaction deleted successfully"
}
```

## 🔑 Understanding Transaction Types

-   **CREDIT**: Represents income or money received. The amount is stored as a positive value.
-   **DEBIT**: Represents expenses or money spent. The amount is automatically converted to a negative value when saved.

## 🧪 Testing the API

### Using cURL

**Register a user:**

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
```

**Login:**

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

**Create a transaction:**

```bash
curl -X POST http://localhost:8000/api/transactions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{"title": "Coffee", "amount": 5, "transaction_type": "DEBIT"}'
```

### Using Python

A verification script is included in the project:

```bash
python verify_auth.py
```

### Using Postman or Thunder Client

1. Import the API endpoints into your preferred API testing tool
2. Create a new user via the `/api/register/` endpoint
3. Login via `/api/login/` to get your access token
4. Use the access token in the Authorization header for protected endpoints

## 📁 Project Structure

```
drf_basic/
├── api/                    # API app for authentication
│   ├── serializers.py      # User registration serializer
│   ├── views.py            # Registration view
│   └── urls.py             # API URL routing
├── core/                   # Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── expense/                # Expense tracking app
│   ├── models.py           # Transaction model
│   ├── serializers.py      # Transaction serializer
│   ├── views.py            # Transaction CRUD views
│   └── tests.py            # Unit tests
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
└── db.sqlite3              # SQLite database (created after migrations)
```

## 🛠️ Technology Stack

-   **Django 5.2.8** - High-level Python web framework
-   **Django REST Framework 3.16.1** - Toolkit for building Web APIs
-   **djangorestframework-simplejwt 5.5.1** - JWT authentication for DRF
-   **SQLite** - Lightweight database (default)
-   **Python 3.12** - Programming language

## 🔒 Security Notes

⚠️ **Important for Production:**

1. **Change the SECRET_KEY**: The current secret key in `settings.py` is for development only. Generate a new one for production:

    ```python
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    ```

2. **Set DEBUG to False**: In production, set `DEBUG = False` in `settings.py`

3. **Configure ALLOWED_HOSTS**: Add your domain to `ALLOWED_HOSTS` in `settings.py`:

    ```python
    ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
    ```

4. **Use Environment Variables**: Store sensitive information in environment variables, not in code

5. **Use a Production Database**: Consider PostgreSQL or MySQL instead of SQLite for production

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

### Common Issues

**Issue: "No such table: expense_transactions"**

-   Solution: Run migrations: `python manage.py migrate`

**Issue: "Authentication credentials were not provided"**

-   Solution: Make sure you're including the JWT token in the Authorization header

**Issue: "Token is invalid or expired"**

-   Solution: Use the refresh token endpoint to get a new access token

**Issue: Docker container exits immediately**

-   Solution: Check if migrations ran successfully. You may need to run migrations manually after container starts

## 📧 Contact

For questions or support, please open an issue in the repository.

---

Made with ❤️ using Django REST Framework
