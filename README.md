# ALX Project Nexus - Job Board API

## Project Overview

ALX Project Nexus is a comprehensive job board platform built with Django and Django REST Framework. The platform connects job seekers with employers through a robust API that handles the complete job application lifecycle. The system features three distinct user roles (Admin, Employer, and Job Seeker), each with specific permissions and capabilities.

The platform enables employers to create company profiles, manage multiple job locations, and post job openings across various industries. Job seekers can browse available positions, submit applications with resumes and cover letters, and track their application status in real-time. Employers can review applications, update candidate status, and manage their hiring pipeline efficiently.

Built with security and scalability in mind, the API uses JWT token authentication, implements role-based access control, and follows RESTful design principles. The modular architecture is organized into three main applications: Accounts (user management), Jobs (job posting and company management), and Applications (application tracking and review).

## Technology Stack

- **Backend Framework**: Django 4.x
- **API Framework**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Database**: PostgreSQL/MySQL (configurable, SQLite for development)
- **File Storage**: Django File Storage
- **Filtering**: django-filter

## Project Structure

```
alx-project-nexus/
├── accounts/              # User authentication and profiles
│   ├── models.py         # User and UserProfile models
│   ├── serializers.py    # Authentication serializers
│   ├── views.py          # Register and Login viewsets
│   ├── urls.py           # Authentication routes
│   └── permissions.py    # Custom permissions
├── applications/         # Job application management
│   ├── models.py         # ApplyJob model
│   ├── serializers.py    # Application serializers
│   ├── views.py          # Application viewsets
│   ├── urls.py           # Application routes
│   └── permissions.py    # Application permissions
├── jobs/                 # Job posting and management
│   ├── models.py         # Industry, Location, Company, Job models
│   ├── serializers.py    # Job-related serializers
│   ├── views.py          # Job management viewsets
│   ├── urls.py           # Job routes
│   └── permissions.py    # Job permissions
├── requirements.txt      # Project dependencies
└── manage.py
```

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)
- PostgreSQL/MySQL (optional, SQLite works for development)

### Setup Instructions

1. **Clone the repository**
```bash
git clone git@github.com:LinusBwana/alx-project-nexus.git
cd alx-project-nexus
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database settings**
Edit `settings.py` to configure your database connection.

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Root URLs Configuration

**Main `urls.py`:**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('applications.urls')),
    path('', include('jobs.urls')),
]
```

### Accounts App URLs

**accounts/urls.py:**
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, LoginViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = [
    path('api/auth/', include(router.urls)), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

**Endpoints:**
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Jobs App URLs

**jobs/urls.py:**
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndustryViewset, LocationViewset, CompanyViewset, PostJobViewset, AvailableJobsViewset

router = DefaultRouter()
router.register(r'industries', IndustryViewset, basename='industries')
router.register(r'locations', LocationViewset, basename='locations')
router.register(r'companies', CompanyViewset, basename='companies')
router.register(r'postjobs', PostJobViewset, basename='postjobs')
router.register(r'availablejobs', AvailableJobsViewset, basename='availablejobs')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

**Endpoints:**
- `GET /api/industries/` - List all industries (Admin only)
- `POST /api/industries/` - Create industry (Admin only)
- `GET /api/industries/{id}/` - Retrieve industry (Admin only)
- `PUT/PATCH /api/industries/{id}/` - Update industry (Admin only)
- `DELETE /api/industries/{id}/` - Delete industry (Admin only)
- `GET /api/locations/` - List user's locations (Employer only)
- `POST /api/locations/` - Create location (Employer only)
- `GET /api/locations/{id}/` - Retrieve location (Employer only)
- `PUT/PATCH /api/locations/{id}/` - Update location (Employer only)
- `DELETE /api/locations/{id}/` - Delete location (Employer only)
- `GET /api/companies/` - List user's companies (Employer only)
- `POST /api/companies/` - Create company (Employer only)
- `GET /api/companies/{id}/` - Retrieve company (Employer only)
- `PUT/PATCH /api/companies/{id}/` - Update company (Employer only)
- `DELETE /api/companies/{id}/` - Delete company (Employer only)
- `GET /api/postjobs/` - List user's posted jobs (Employer only)
- `POST /api/postjobs/` - Create job posting (Employer only)
- `GET /api/postjobs/{id}/` - Retrieve job (Employer only)
- `PUT/PATCH /api/postjobs/{id}/` - Update job (Employer only)
- `DELETE /api/postjobs/{id}/` - Delete job (Employer only)
- `GET /api/availablejobs/` - List all active jobs (Public)
- `GET /api/availablejobs/{id}/` - Retrieve job details (Public)

### Applications App URLs

**applications/urls.py:**
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplyJobViewset, MyApplicationHistoryViewset, JobApplicationsHistoryViewset

router = DefaultRouter()
router.register(r'apply-job', ApplyJobViewset, basename='apply-job')
router.register(r'my-applications-history', MyApplicationHistoryViewset, basename='my-applications')
router.register(r'job-applications-history', JobApplicationsHistoryViewset, basename='job-applications')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

**Endpoints:**
- `POST /api/apply-job/` - Submit job application (Job Seeker only)
- `GET /api/my-applications-history/` - View own applications (Job Seeker only)
- `GET /api/my-applications-history/{id}/` - View application details (Job Seeker only)
- `GET /api/job-applications-history/` - View applications to own jobs (Employer only)
- `GET /api/job-applications-history/{id}/` - View application details (Employer only)
- `PUT/PATCH /api/job-applications-history/{id}/` - Update application status (Employer only)

## API Request and Response Examples

### Accounts App

#### Register User (POST)
**Endpoint:** `POST /api/auth/register/`

**Request:**
```json
{
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone_number": "+254712345678",
  "role": "job_seeker",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}
```

**Response:** `201 Created`
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone_number": "+254712345678",
  "role": "job_seeker"
}
```

#### Login User (POST)
**Endpoint:** `POST /api/auth/login/`

**Request:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjM5NjgwMCwiaWF0IjoxNzMyMzEwNDAwLCJqdGkiOiJhYmNkZWYxMjM0NTYiLCJ1c2VyX2lkIjoiYTFiMmMzZDQtZTVmNi03ODkwLWFiY2QtZWYxMjM0NTY3ODkwIn0.xyz123abc456",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMzE0MDAwLCJpYXQiOjE3MzIzMTA0MDAsImp0aSI6ImFiY2RlZjEyMzQ1NiIsInVzZXJfaWQiOiJhMWIyYzNkNC1lNWY2LTc4OTAtYWJjZC1lZjEyMzQ1Njc4OTAifQ.abc123xyz456",
  "user": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone_number": "+254712345678",
    "role": "job_seeker"
  }
}
```

### Jobs App

#### List Available Jobs (GET - Public)
**Endpoint:** `GET /api/availablejobs/`

**Response:** `200 OK`
```json
[
  {
    "id": "job123-uuid-here",
    "title": "Senior Software Engineer",
    "slug": "senior-software-engineer-tech-innovations-ltd-a1b2",
    "company": "company123-uuid-here",
    "industry": "industry123-uuid-here",
    "location": ["location123-uuid-here"],
    "job_type": "full_time",
    "experience_level": "senior",
    "description": "We are looking for an experienced software engineer...",
    "requirements": "Bachelor's degree in Computer Science, 5+ years of experience...",
    "responsibilities": "Design and develop scalable applications, Lead technical projects...",
    "skills_required": "Python, Django, REST API, PostgreSQL, Docker",
    "salary_min": "100000.00",
    "salary_max": "150000.00",
    "salary_currency": "KES",
    "is_salary_visible": true,
    "posted_by": "employer123-uuid-here",
    "is_active": true,
    "application_deadline": "2025-12-31",
    "posted_on": "2025-11-15T10:30:00Z",
    "updated_on": "2025-11-15T10:30:00Z"
  },
  {
    "id": "job456-uuid-here",
    "title": "Frontend Developer",
    "slug": "frontend-developer-creative-agency-x9y8",
    "company": "company456-uuid-here",
    "industry": "industry456-uuid-here",
    "location": ["location456-uuid-here"],
    "job_type": "full_time",
    "experience_level": "mid_level",
    "description": "Join our creative team to build amazing user experiences...",
    "requirements": "3+ years experience with React, Strong CSS skills...",
    "responsibilities": "Build responsive web applications, Collaborate with designers...",
    "skills_required": "React, TypeScript, CSS, HTML, Git",
    "salary_min": "70000.00",
    "salary_max": "100000.00",
    "salary_currency": "KES",
    "is_salary_visible": true,
    "posted_by": "employer456-uuid-here",
    "is_active": true,
    "application_deadline": "2025-11-30",
    "posted_on": "2025-11-10T14:20:00Z",
    "updated_on": "2025-11-10T14:20:00Z"
  }
]
```

#### Create Industry (POST - Admin Only)
**Endpoint:** `POST /api/industries/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "name": "Information Technology",
  "description": "Technology and software development sector including hardware, software, and IT services"
}
```

**Response:** `201 Created`
```json
{
  "id": "industry123-uuid-here",
  "name": "Information Technology",
  "slug": "information-technology",
  "description": "Technology and software development sector including hardware, software, and IT services",
  "is_active": true,
  "created_at": "2025-11-15T09:00:00Z",
  "updated_at": "2025-11-15T09:00:00Z"
}
```

**Error Response (Non-Admin User):** `403 Forbidden`
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### Create Location (POST - Employer Only)
**Endpoint:** `POST /api/locations/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "country": "Kenya",
  "city": "Nairobi",
  "region": "Nairobi County",
  "is_remote": false
}
```

**Response:** `201 Created`
```json
{
  "id": "location123-uuid-here",
  "country": "Kenya",
  "city": "Nairobi",
  "region": "Nairobi County",
  "is_remote": false,
  "created_at": "2025-11-15T10:00:00Z"
}
```

#### Get User's Locations (GET - Employer Only)
**Endpoint:** `GET /api/locations/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
[
  {
    "id": "location123-uuid-here",
    "country": "Kenya",
    "city": "Nairobi",
    "region": "Nairobi County",
    "is_remote": false,
    "created_at": "2025-11-15T10:00:00Z"
  },
  {
    "id": "location456-uuid-here",
    "country": "Kenya",
    "city": "Mombasa",
    "region": "Mombasa County",
    "is_remote": false,
    "created_at": "2025-11-16T11:00:00Z"
  }
]
```

#### Create Company (POST - Employer Only)
**Endpoint:** `POST /api/companies/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request:**
```json
{
  "name": "Tech Innovations Ltd",
  "description": "Leading technology company specializing in cloud solutions and enterprise software",
  "website_url": "https://techinnovations.com",
  "industry": "industry123-uuid-here",
  "locations": ["location123-uuid-here", "location456-uuid-here"]
}
```

**Response:** `201 Created`
```json
{
  "id": "company123-uuid-here",
  "name": "Tech Innovations Ltd",
  "slug": "tech-innovations-ltd-leading-technology-company-spec-z9x8",
  "locations": ["location123-uuid-here", "location456-uuid-here"],
  "description": "Leading technology company specializing in cloud solutions and enterprise software",
  "logo": null,
  "website_url": "https://techinnovations.com",
  "industry": "industry123-uuid-here",
  "is_verified": false,
  "created_at": "2025-11-15T11:00:00Z",
  "updated_at": "2025-11-15T11:00:00Z",
  "created_by": "employer123-uuid-here"
}
```

**Error Response (No Locations Created):** `403 Forbidden`
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### Post Job (POST - Employer Only)
**Endpoint:** `POST /api/postjobs/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "title": "Senior Software Engineer",
  "company": "company123-uuid-here",
  "location": ["location123-uuid-here"],
  "job_type": "full_time",
  "experience_level": "senior",
  "description": "We are looking for an experienced software engineer to join our growing team...",
  "requirements": "Bachelor's degree in Computer Science or related field, 5+ years of software development experience, Strong problem-solving skills",
  "responsibilities": "Design and develop scalable applications, Lead technical projects, Mentor junior developers, Code review and quality assurance",
  "skills_required": "Python, Django, REST API, PostgreSQL, Docker, AWS",
  "salary_min": "100000.00",
  "salary_max": "150000.00",
  "salary_currency": "KES",
  "is_salary_visible": true,
  "application_deadline": "2025-12-31"
}
```

**Response:** `201 Created`
```json
{
  "id": "job123-uuid-here",
  "title": "Senior Software Engineer",
  "slug": "senior-software-engineer-tech-innovations-ltd-a1b2",
  "company": "company123-uuid-here",
  "industry": "industry123-uuid-here",
  "location": ["location123-uuid-here"],
  "job_type": "full_time",
  "experience_level": "senior",
  "description": "We are looking for an experienced software engineer to join our growing team...",
  "requirements": "Bachelor's degree in Computer Science or related field, 5+ years of software development experience, Strong problem-solving skills",
  "responsibilities": "Design and develop scalable applications, Lead technical projects, Mentor junior developers, Code review and quality assurance",
  "skills_required": "Python, Django, REST API, PostgreSQL, Docker, AWS",
  "salary_min": "100000.00",
  "salary_max": "150000.00",
  "salary_currency": "KES",
  "is_salary_visible": true,
  "posted_by": "employer123-uuid-here",
  "is_active": true,
  "application_deadline": "2025-12-31",
  "posted_on": "2025-11-15T12:00:00Z",
  "updated_on": "2025-11-15T12:00:00Z"
}
```

**Error Response (No Company Created):** `403 Forbidden`
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Applications App

#### Apply for Job (POST - Job Seeker Only)
**Endpoint:** `POST /api/apply-job/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request:**
```json
{
  "job": "job123-uuid-here",
  "cover_letter": "I am writing to express my strong interest in the Senior Software Engineer position at Tech Innovations Ltd. With over 6 years of experience in software development and a proven track record of delivering high-quality solutions...",
  "resume": "file_upload_here.pdf",
  "additional_documents": "portfolio_file.pdf",
  "experience_years": 6,
  "expected_salary": "130000.00",
  "availability_date": "2026-01-15"
}
```

**Response:** `201 Created`
```json
{
  "id": "application123-uuid-here",
  "job": "job123-uuid-here",
  "applicant": "jobseeker123-uuid-here",
  "status": "pending",
  "cover_letter": "I am writing to express my strong interest in the Senior Software Engineer position at Tech Innovations Ltd. With over 6 years of experience in software development and a proven track record of delivering high-quality solutions...",
  "resume": "/media/application_documents/user_jobseeker123-uuid-here/resume_john_doe.pdf",
  "additional_documents": "/media/application_documents/user_jobseeker123-uuid-here/portfolio.pdf",
  "experience_years": 6,
  "expected_salary": "130000.00",
  "availability_date": "2026-01-15",
  "reviewed_by": null,
  "reviewed_at": null,
  "applied_on": "2025-11-19T14:30:00Z"
}
```

**Error Response (Employer Trying to Apply):** `403 Forbidden`
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### Get My Applications (GET - Job Seeker Only)
**Endpoint:** `GET /api/my-applications-history/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
[
  {
    "id": "application123-uuid-here",
    "job_title": "Senior Software Engineer",
    "company_name": "Tech Innovations Ltd",
    "job_location": "Kenya, Nairobi, Nairobi County",
    "status": "pending"
  },
  {
    "id": "application456-uuid-here",
    "job_title": "Frontend Developer",
    "company_name": "Creative Agency",
    "job_location": "Kenya, Mombasa, Mombasa County",
    "status": "reviewed"
  },
  {
    "id": "application789-uuid-here",
    "job_title": "DevOps Engineer",
    "company_name": "Cloud Solutions Inc",
    "job_location": "Kenya, Nairobi, Nairobi County - Remote",
    "status": "shortlisted"
  }
]
```

#### Get Applications to My Jobs (GET - Employer Only)
**Endpoint:** `GET /api/job-applications-history/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
[
  {
    "id": "application123-uuid-here",
    "job": "job123-uuid-here",
    "job_title": "Senior Software Engineer",
    "applicant_name": "John Doe",
    "applicant_email": "john@example.com",
    "job_location": "Kenya, Nairobi, Nairobi County",
    "status": "pending",
    "applied_on": "2025-11-19T14:30:00Z",
    "experience_years": 6,
    "expected_salary": "130000.00",
    "cover_letter": "I am writing to express my strong interest in the Senior Software Engineer position...",
    "resume": "/media/application_documents/user_jobseeker123-uuid-here/resume_john_doe.pdf"
  },
  {
    "id": "application456-uuid-here",
    "job": "job123-uuid-here",
    "job_title": "Senior Software Engineer",
    "applicant_name": "Jane Smith",
    "applicant_email": "jane@example.com",
    "job_location": "Kenya, Nairobi, Nairobi County",
    "status": "reviewed",
    "applied_on": "2025-11-18T10:15:00Z",
    "experience_years": 7,
    "expected_salary": "140000.00",
    "cover_letter": "With 7 years of experience in full-stack development...",
    "resume": "/media/application_documents/user_jobseeker456-uuid-here/resume_jane_smith.pdf"
  }
]
```

#### Update Application Status (PATCH - Employer Only)
**Endpoint:** `PATCH /api/job-applications-history/{application_id}/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "status": "shortlisted"
}
```

**Response:** `200 OK`
```json
{
  "id": "application123-uuid-here",
  "job": "job123-uuid-here",
  "job_title": "Senior Software Engineer",
  "applicant_name": "John Doe",
  "applicant_email": "john@example.com",
  "job_location": "Kenya, Nairobi, Nairobi County",
  "status": "shortlisted",
  "applied_on": "2025-11-19T14:30:00Z",
  "experience_years": 6,
  "expected_salary": "130000.00",
  "cover_letter": "I am writing to express my strong interest in the Senior Software Engineer position...",
  "resume": "/media/application_documents/user_jobseeker123-uuid-here/resume_john_doe.pdf"
}
```

**Error Response (Job Seeker Trying to Update):** `403 Forbidden`
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**Error Response (Employer Updating Another Employer's Job Application):** `403 Forbidden`
```json
{
  "detail": "You do not have permission to perform this action."
}
```

## Authentication

All protected endpoints require a JWT access token in the Authorization header:

```
Authorization: Bearer {access_token}
```

### Token Refresh
When the access token expires, use the refresh token to obtain a new one:

**Endpoint:** `POST /api/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Permissions Summary

### User Roles
- **Admin**: Manage industries, full platform access
- **Employer**: Create companies, post jobs, review applications
- **Job Seeker**: Browse jobs, apply for positions, track applications

### Permission Rules
1. **Employers must create a location before creating a company**
2. **Employers must own a company before posting jobs**
3. **Job seekers can only apply to active jobs before the deadline**
4. **Only authenticated job seeker can apply for active jobs**
5. **Job seeks can view only their job application history**
6. **Users can only manage their own resources** (locations, companies, jobs, applications)
7. **Only job owners can update application status**
8. **Job owners can only view history of application made to their jobs**

## Search and Filtering

Search functionality is available on multiple endpoints:

```bash
GET /api/availablejobs/?search=python+developer
GET /api/availablejobs/?search=remote
GET /api/companies/?search=tech
GET /api/postjobs/?search=senior+engineer
```

## Status Codes

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Authentication required or invalid token
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Security Features

- JWT token-based authentication
- Password hashing with Django's built-in password validators
- Role-based access control (RBAC)
- Object-level permissions
- CSRF protection
- SQL injection prevention through Django ORM
- File upload validation

## Swagger Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

Linus Bwana - [@LinusBwana](https://github.com/LinusBwana)

## Support

For support, open an issue in the GitHub repository: https://github.com/LinusBwana/alx-project-nexus/issues

---

**Note:** This is a backend API. A separate frontend application is required for the complete user interface.