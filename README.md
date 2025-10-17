# 🎓 University Exam Application Tracking System

A comprehensive Django-based web application for managing and tracking university exam applications (resit, retake, and special exams) with automated document verification, multi-role dashboards, and real-time status tracking.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-4.2%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [User Roles](#user-roles)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The University Exam Application Tracking System streamlines the process of applying for and managing supplementary examinations at Kenyan universities. The system provides:

- **Students**: Easy application submission with document upload
- **Exam Officers**: Efficient review and approval workflows
- **Lecturers**: Simplified exam marking and grade submission
- **Automated OCR**: Document verification using text extraction
- **Real-time Tracking**: Live status updates and notifications

---

## ✨ Features

### Core Functionality

#### 🎓 Student Portal
- Submit exam applications (resit/retake/special exams)
- Upload supporting documents (medical certificates, approval letters)
- Track application status in real-time
- Receive notifications at each stage
- View exam results when published

#### 👨‍💼 Exam Officer Dashboard
- Review submitted applications
- Verify OCR-extracted document data
- Approve or reject applications with comments
- Assign applications to appropriate lecturers
- Monitor overall application statistics
- Generate reports and analytics

#### 👨‍🏫 Lecturer Portal
- View assigned exam applications
- Receive and acknowledge exam scripts
- Submit marks and feedback
- Track marking progress
- Communicate with exam office

#### 🤖 Automated Features
- **OCR Document Verification**: Automatic text extraction from uploaded documents
- **Smart Assignment**: Auto-assign applications to lecturers based on unit assignments
- **Email Notifications**: Automated email alerts for status changes
- **Audit Trail**: Complete history of all application actions

### Additional Features
- Multi-school support (Business, Engineering, Science, etc.)
- Semester-based tracking
- Comprehensive search and filtering
- Export functionality (CSV, PDF reports)
- Role-based access control
- Responsive design for mobile access

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Django Application                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Student    │  │ Exam Officer │  │   Lecturer   │  │
│  │   Portal     │  │   Dashboard  │  │   Portal     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Application Logic Layer                │ │
│  │  - Authentication & Authorization                   │ │
│  │  - Business Logic & Validation                      │ │
│  │  - OCR Processing & Document Verification           │ │
│  │  - Notification Service                             │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │                  Data Layer (ORM)                   │ │
│  │  - Models & Relationships                           │ │
│  │  - Queries & Aggregations                           │ │
│  │  - Signals & Hooks                                  │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │   PostgreSQL     │
                  │    Database      │
                  └──────────────────┘
```

---

## 💻 Technology Stack

### Backend
- **Framework**: Django 4.2+
- **Language**: Python 3.8+
- **Database**: PostgreSQL 13+ (SQLite for development)
- **Authentication**: Django Auth with custom user profiles

### Frontend
- **Templates**: Django Templates
- **CSS Framework**: Bootstrap 5 / Tailwind CSS
- **JavaScript**: Vanilla JS / jQuery
- **Icons**: Font Awesome

### Additional Tools
- **OCR**: Tesseract OCR / Google Cloud Vision API
- **File Storage**: Django FileField (local) / AWS S3 (production)
- **Task Queue**: Celery (for async OCR processing)
- **Email**: Django Email Backend / SendGrid

---

## 🚀 Installation

### Prerequisites
```bash
Python 3.8+
pip
virtualenv
PostgreSQL 13+ (optional, for production)
Git
```

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/exam-tracking-system.git
cd exam-tracking-system
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/exam_db
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# OCR Configuration (optional)
GOOGLE_CLOUD_VISION_API_KEY=your-api-key
```

### Step 5: Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed database with sample data
python manage.py seed_data
```

### Step 6: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## ⚙️ Configuration

### Database Configuration

#### SQLite (Development)
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### PostgreSQL (Production)
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'exam_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### File Upload Settings
```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Maximum file upload size (10MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760
```

### Email Configuration
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
```

---

## 📖 Usage

### Default Login Credentials (After Seeding)

#### Students
- Username: `student1` to `student50`
- Password: `student123`
- Example: `student1` / `student123`

#### Exam Officers
- Username: `officer1` to `officer8`
- Password: `officer123`
- Example: `officer1` / `officer123`

#### Lecturers
- Username: `lecturer1` to `lecturer16`
- Password: `lecturer123`
- Example: `lecturer1` / `lecturer123`

### Application Workflow

1. **Student Submission**
   - Student logs in and navigates to "New Application"
   - Fills in exam details (unit code, exam type, year/semester)
   - Uploads supporting document
   - Accepts declaration and submits

2. **OCR Processing**
   - System extracts text from uploaded document
   - Verifies key information (student details, unit code)
   - Calculates confidence score

3. **Officer Review**
   - Exam officer reviews application and OCR results
   - Verifies document authenticity
   - Approves or rejects with comments
   - System auto-assigns to appropriate lecturer

4. **Lecturer Marking**
   - Lecturer acknowledges receipt of exam script
   - Marks exam and enters grade
   - Submits marks back to exam office

5. **Result Publication**
   - Officer verifies marks
   - Uploads to student portal
   - Student receives notification

---

## 👥 User Roles

### Student
**Permissions:**
- Submit exam applications
- View own applications
- Track application status
- Receive notifications
- View published results

### Exam Officer
**Permissions:**
- View all applications (department-specific or all)
- Review and approve/reject applications
- Assign applications to lecturers
- Monitor application statistics
- Generate reports
- Communicate with students and lecturers

### Lecturer
**Permissions:**
- View assigned applications
- Acknowledge exam receipt
- Submit marks and feedback
- Track marking progress
- Communicate with exam office

### Admin/Superuser
**Permissions:**
- Full system access
- User management
- System configuration
- Database management
- Access Django admin panel

---

## 🗄️ Database Schema

### Core Models

#### User Management
- `User` (Django built-in)
- `UserProfile` - Base profile for all users
- `Student` - Student-specific information
- `ExamOfficer` - Exam officer details
- `Lecturer` - Lecturer details

#### Academic Structure
- `UnitAssignment` - Lecturer-unit mappings

#### Application Management
- `ExamApplication` - Main application record
- `OCRResult` - Document verification results
- `ApplicationReview` - Officer review records
- `ExamMarking` - Lecturer marking records

#### Communication
- `Notification` - Student notifications

### Key Relationships
```
User (1) ──────── (1) UserProfile
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    Student       ExamOfficer      Lecturer
        │               │               │
        │               │               └──── UnitAssignment
        │               │
        └───── ExamApplication ──────┐
                    │                │
                    ├── OCRResult    │
                    ├── ApplicationReview
                    ├── ExamMarking  │
                    └── Notification ┘
```

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/login/          - User login
POST   /api/auth/logout/         - User logout
POST   /api/auth/register/       - User registration
```

### Student Endpoints
```
GET    /api/applications/        - List student's applications
POST   /api/applications/        - Submit new application
GET    /api/applications/{id}/   - Get application details
GET    /api/notifications/       - Get notifications
PATCH  /api/notifications/{id}/  - Mark as read
```

### Officer Endpoints
```
GET    /api/officer/applications/        - List pending applications
PATCH  /api/officer/applications/{id}/   - Review application
POST   /api/officer/assign/              - Assign to lecturer
GET    /api/officer/statistics/          - Dashboard stats
```

### Lecturer Endpoints
```
GET    /api/lecturer/applications/       - List assigned applications
POST   /api/lecturer/acknowledge/{id}/   - Acknowledge receipt
POST   /api/lecturer/submit-marks/{id}/  - Submit marks
```

---

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific Test Module
```bash
python manage.py test exam_portal.tests.test_models
python manage.py test exam_portal.tests.test_views
```

### Generate Coverage Report
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Sample Test Files Structure
```
exam_portal/
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_views.py
    ├── test_forms.py
    └── test_services.py
```

---

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL database
- [ ] Set up static file serving (WhiteNoise/Nginx)
- [ ] Configure media file storage (AWS S3)
- [ ] Set up email service (SendGrid/AWS SES)
- [ ] Enable HTTPS/SSL
- [ ] Set strong `SECRET_KEY`
- [ ] Configure logging
- [ ] Set up backup strategy
- [ ] Enable security middleware
- [ ] Configure CORS if using APIs

### Deployment Options

#### Heroku
```bash
# Install Heroku CLI
heroku login
heroku create exam-tracking-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### DigitalOcean/AWS
```bash
# Use gunicorn as WSGI server
pip install gunicorn

# Create Procfile
echo "web: gunicorn your_project.wsgi" > Procfile

# Configure Nginx reverse proxy
# Set up systemd service
# Configure PostgreSQL
```

#### Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "your_project.wsgi:application"]
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Write unit tests for new features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Django documentation and community
- Kenyan university exam management systems
- Contributors and testers

---

## 📞 Support

For support, email support@examtracking.ac.ke or open an issue on GitHub.

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] REST API with DRF
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Bulk upload for officers
- [ ] SMS notifications
- [ ] Payment gateway integration
- [ ] Multi-language support
- [ ] AI-powered document verification

---

## 📊 System Requirements

### Minimum
- 2GB RAM
- 10GB Storage
- 2 CPU Cores
- Python 3.8+

### Recommended
- 4GB RAM
- 50GB Storage
- 4 CPU Cores
- Python 3.10+
- PostgreSQL 14+

---

**Built with Janet & Steve for Kenyan Universities**