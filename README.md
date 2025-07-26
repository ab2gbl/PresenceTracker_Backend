# Presence Tracker API Documentation

A Django REST API for managing employee presence tracking in companies.

## Base URL
```
http://localhost:8000/
```

## Authentication
This API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 🔐 Authentication Endpoints

### 1. User Registration
**POST** `/user/register/`

Register a new company owner account.

**Request Body:**
```json
{
  "username": "company_owner",
  "email": "owner@company.com",
  "password": "securepassword123",
  "password2": "securepassword123"
}
```

**Response (201):**
```json
{
  "id": 1,
  "username": "company_owner",
  "email": "owner@company.com"
}
```

### 2. Login (Get JWT Token)
**POST** `/user/api/token/`

Authenticate and receive JWT tokens.

**Request Body:**
```json
{
  "username": "company_owner",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Refresh Token
**POST** `/user/api/token/refresh/`

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 4. Verify Token
**POST** `/user/api/token/verify/`

**Request Body:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 🏢 Company Management

### 1. Create Company
**POST** `/presence/companies/`

Create a new company (authenticated user becomes the owner).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "Tech Solutions Inc",
  "address": "123 Business Street, City, State",
  "phone": "+1234567890",
  "email": "contact@techsolutions.com",
  "website": "https://techsolutions.com"
}
```

**Response (201):**
```json
{
  "name": "Tech Solutions Inc",
  "address": "123 Business Street, City, State",
  "phone": "+1234567890",
  "email": "contact@techsolutions.com",
  "website": "https://techsolutions.com",
  "date_created": "2025-07-26",
  "owner": "company_owner"
}
```

### 2. List Companies
**GET** `/presence/companies/`

Get all companies (only authenticated users).

**Headers:**
```
Authorization: Bearer <token>
```

### 3. Get Company Details
**GET** `/presence/companies/{id}/`

**Headers:**
```
Authorization: Bearer <token>
```

### 4. Update Company
**PUT/PATCH** `/presence/companies/{id}/`

Only company owner or staff can update.

### 5. Delete Company
**DELETE** `/presence/companies/{id}/`

Only company owner or staff can delete.

---

## 👥 Employee Management

### 1. Register Employee
**POST** `/presence/employees/`

Add a new employee to a company.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@company.com",
  "phone": "+1234567890",
  "position": "Software Developer",
  "company": 1,
  "is_active": true
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@company.com",
  "phone": "+1234567890",
  "position": "Software Developer",
  "date_joined": "2025-07-26",
  "is_active": true,
  "company": 1
}
```

### 2. List All Employees
**GET** `/presence/employees/`

**Headers:**
```
Authorization: Bearer <token>
```

### 3. Get Company Employees
**GET** `/presence/companies/{company_id}/employees/`

Get all employees for a specific company (only company owner can access).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@company.com",
    "phone": "+1234567890",
    "position": "Software Developer",
    "date_joined": "2025-07-26",
    "is_active": true,
    "company": 1
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@company.com",
    "phone": "+1987654321",
    "position": "UI/UX Designer",
    "date_joined": "2025-07-25",
    "is_active": true,
    "company": 1
  }
]
```

### 4. Get Employee Details
**GET** `/presence/employees/{id}/`

### 5. Update Employee
**PUT/PATCH** `/presence/employees/{id}/`

### 6. Delete Employee
**DELETE** `/presence/employees/{id}/`

---

## ✅ Attendance Management

### 1. Mark Attendance
**POST** `/presence/attendance/`

Record employee attendance for a specific date.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "employee": 1,
  "date": "2025-07-26",
  "is_present": true,
  "note": "On time"
}
```

**Response (201):**
```json
{
  "id": 1,
  "employee": 1,
  "date": "2025-07-26",
  "is_present": true,
  "note": "On time"
}
```

### 2. Get Attendance Details
**GET** `/presence/attendance/{id}/`

**Headers:**
```
Authorization: Bearer <token>
```

### 3. Update Attendance
**PUT/PATCH** `/presence/attendance/{id}/`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "is_present": false,
  "note": "Sick leave"
}
```

### 4. Delete Attendance Record
**DELETE** `/presence/attendance/{id}/`

### 5. Get Attendance List (Reports)
**GET** `/presence/attendance/list/`

Get attendance records with filtering options.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `company_id` (optional): Filter by company ID
- `employee_id` (optional): Filter by employee ID

**Example Request:**
```
GET /presence/attendance/list/?start_date=2025-07-01&end_date=2025-07-31&company_id=1
```

**Response (200):**
```json
[
  {
    "id": 1,
    "employee": 1,
    "date": "2025-07-26",
    "is_present": true,
    "note": "On time"
  },
  {
    "id": 2,
    "employee": 2,
    "date": "2025-07-26",
    "is_present": false,
    "note": "Sick leave"
  }
]
```

---

## 🔒 Permissions

### Company Owner Permissions:
- ✅ Create, read, update, delete their own company
- ✅ Add, view, edit, delete employees in their company
- ✅ Mark attendance for their employees
- ✅ View attendance reports for their company
- ❌ Cannot access other companies' data

### Staff/Admin Permissions:
- ✅ Full access to all companies and data
- ✅ Can perform all CRUD operations

### Security Features:
- JWT token authentication required for all endpoints
- Company owners can only access their own data
- Unique constraint on employee attendance per date
- Input validation and error handling

---

## 📊 Response Status Codes

- `200 OK` - Successful GET, PUT, PATCH requests
- `201 Created` - Successful POST requests
- `204 No Content` - Successful DELETE requests
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## 🔧 Error Response Format

```json
{
  "detail": "Error message description",
  "field_errors": {
    "field_name": ["Specific field error message"]
  }
}
```

---

## 🚀 Quick Start Guide

1. **Register a company owner:**
   ```bash
   POST /user/register/
   ```

2. **Login to get JWT token:**
   ```bash
   POST /user/api/token/
   ```

3. **Create your company:**
   ```bash
   POST /presence/companies/
   ```

4. **Add employees:**
   ```bash
   POST /presence/employees/
   ```

5. **Mark daily attendance:**
   ```bash
   POST /presence/attendance/
   ```

6. **View attendance reports:**
   ```bash
   GET /presence/attendance/list/?start_date=2025-07-01&end_date=2025-07-31&company_id=1
   ```
