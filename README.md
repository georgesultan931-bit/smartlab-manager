# SmartLab Manager

SmartLab Manager is a Django-based lab and student/patient record management system for managing registrations, test requests, results, PDF reports, dashboards, and audit logs.

## Features
- Role-based authentication (Admin, Lab Technician, Receptionist)
- Patient/student registration and profile management
- Test type and test request management
- Result entry and updates
- PDF report generation with WeasyPrint
- Dashboard with summary stats
- Audit logging for create, update, delete, and login events
- Search and filtering for patients and test requests

## Stack
- Django
- Bootstrap 5 (CDN)
- SQLite by default, PostgreSQL supported via environment variables
- WeasyPrint for PDF generation

## Quick start
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env  # or cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py runserver
```

## Default demo accounts after seeding
- admin / admin12345
- labtech / admin12345
- reception / admin12345

## Main modules
- `apps.accounts` – custom user model and auth hooks
- `apps.patients` – patient/student registration
- `apps.tests` – test types and test requests
- `apps.results` – result entry and updates
- `apps.reports` – printable and PDF reports
- `apps.dashboard` – dashboard metrics
- `apps.auditlogs` – activity tracking

## Notes
- Uses SQLite by default so it runs immediately after download.
- Set `DB_ENGINE=postgres` and the DB variables in `.env` if you want PostgreSQL.
- For PDF generation, install any required system libraries for WeasyPrint if your OS needs them.
