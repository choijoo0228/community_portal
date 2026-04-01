# Community Portal(Django Cloud Project)

This project is a Community Portal web application built using Django and deployed on AWS.
It allows users to view events, access resources, and suggest new events through a web interface.

The application is designed using a cloud-based architecture with separate services for compute, storage, and database.

## Features

- **Event Management**: Create, view, and manage community events
- **Event Suggestions**: Users can suggest new events for the community
- **Resource Directory**: Browse and manage community resources
- **User Accounts**: Registration and authentication system
- **Media Support**: Upload and manage event and resource images
- **Admin Dashboard**: Manage content through Django admin interface
- **Deployment**: Cload based deployment 

### Main Application
- **Home**: View featured events and resources
- **Events**: Browse all community events
- **Resources**: Access community resources directory
- **Suggest Event**: Submit suggestions for new events
- **My Suggestions**: View your submitted event suggestions

## Project Structure

community_portal/
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── db.sqlite3               # SQLite database for localhost
├── community_portal/        # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── portal/                  # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── urls.py              # App URL routing
│   ├── forms.py             # Django forms
│   ├── templates/           # HTML templates
│   ├── static/              # Static files (CSS, JS)
│   └── migrations/          # Database migrations
├── media/                   # User-uploaded media files/Amazon S3/
└── staticfiles/             # Collected static files

## Architecture

Backend: Django (Python)
Web Server: Gunicorn + Nginx
Cloud Hosting: Amazon EC2
Database: Amazon RDS (PostgreSQL)
Media Storage: Amazon S3
CI/CD: GitHub Actions


Architecture Flow

User → EC2 (Django App) → RDS (Database)
                            ↓
                            S3 (Images)

## Requirements

- Python 3.8+
- Django 4.2+
- PostgreSQL (recommended for production)
- Additional dependencies listed in `requirements.txt`

## Key Dependencies

- **Django**: Web framework
- **Pillow**: Image processing
- **psycopg**: PostgreSQL adapter
- **django-storages**: S3/cloud storage support
- **boto3**: AWS integration
- **gunicorn**: WSGI HTTP server (production)
- **whitenoise**: Static file serving

## Database Configuration

This project uses different databases depending on the environment:

### Local Development

- SQLite (db.sqlite3)
- Automatically created and used by Django
- No external setup required
    
python manage.py migrate

### Production (AWS)

- Uses Amazon RDS (PostgreSQL)
- Provides scalable and managed database services

Configured using environment variables:

DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=your_rds_endpoint
DB_PORT=5432
AWS_ACCESS_KEY_ID=aws_access_key_id
AWS_SECRET_ACCESS_KEY=aws_secret_access_key
AWS_SESSION_TOKEN=aws_session_token
AWS_STORAGE_BUCKET_NAME=your_bucket 
AWS_S3_REGION_NAME=your_region

## Installation /Local/

1. **Clone the repository**

    git clone https://github.com/choijoo0228/community_portal.git 
    cd community_portal

2. **Create and activate a virtual environment**

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate


3. **Install dependencies**

    pip install -r requirements.txt

4. **Run migrations**

    python manage.py migrate

5. **Create a superuser**
    
    python manage.py createsuperuser
    

6. **Run the development server**
    
    python manage.py runserver

The application will be available at `http://localhost:8000`

### Admin Panel
Access the Django admin interface at `http://localhost:8000/admin/` with your superuser credentials.


## AWS Deployment

The application is deployed using:

- EC2 instance for hosting the Django app
- RDS PostgreSQL database for persistent storage
- S3 bucket for storing uploaded images
- Nginx + Gunicorn for serving the application

## CI/CD Pipeline

GitHub Actions is used for continuous integration and deployment.

### Pipeline Workflow:

1. Code pushed to GitHub repository
2. Install dependencies
3. Run static code analysis:
    - ruff (code quality)
    - bandit (security)
    - pip-audit (dependency vulnerabilities)
4. SSH into EC2 instance
5. Deploy application:
    - update code
    - apply migrations
    - collect static files
    - restart services

## Security Considerations

- Environment variables used for sensitive data
- SSH keys excluded from repository (.gitignore)
- S3 bucket configured for:
    - public read access (media files)
    - restricted write access
- HTTPS enforced (recommended)
- Static code analysis tools integrated in CI/CD

## Testing

- Manual testing of all user flows
- Admin panel validation
- CI pipeline ensures code quality and security checks
- Verified integration between EC2, RDS, and S3


## Database Models

- **Event**: Community events with details, images, and scheduling
- **Resource**: Community resources and information
- **EventSuggestion**: User-submitted event suggestions
- **UserProfile**: Extended user information

## Author

Student: Choijoo Erdenesuren
Student ID: x25116380
Institution: National College of Ireland

## License

This project is developed for academic purposes only.
