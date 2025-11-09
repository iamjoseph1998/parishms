# Parish Management System

A comprehensive web application for managing parish activities, members, and administrative tasks.

## Features

- User Authentication with custom roles:
  - Administrator
  - Parish Priest
  - President
  - Vice President
  - Treasurer
  - Body Member
  - Family Head
- Member Management
- Financial Management
- Activity Management

## Technology Stack

- Django
- Django REST Framework
- Postgres
- Python 3

## Setup

1. Clone the repository
```bash
git clone <repository-url>
cd parishms
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Apply migrations
```bash
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run development server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## API Documentation

- API endpoints documentation will be available at `/api/docs/`
- Admin interface is available at `/admin/`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.