# Learning Management System V3

A web application for managing online courses and learning materials.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Screenshots](#screenshots)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)
- [Contact](#contact)

## Technologies Used

- Python 3.9
- Django 3.2.5
- PostgreSQL 13.3
- HTML, CSS, JavaScript

## Installation

1. Clone the repository: `git clone https://github.com/NagiPragalathan/Learning_Management_System_V3.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Create and activate a virtual environment (optional): `python3 -m venv venv` and `source venv/bin/activate`
4. Create a PostgreSQL database and update the database settings in `settings.py`.
5. Run database migrations: `python manage.py migrate`
6. Load initial data: `python manage.py loaddata fixtures/*.json`
7. Start the server: `python manage.py runserver`

## Usage

1. Open the application in a web browser: `http://localhost:8000/`
2. Login with the following credentials:
   - Email: admin@example.com
   - Password: password
3. Create, edit, or delete courses, modules, and learning materials.
4. Assign instructors and students to courses.
5. View course progress and completion status.

## Features

- User authentication and authorization
- Course management (create, edit, delete)
- Module management (create, edit, delete)
- Learning material management (create, edit, delete)
- Instructor and student management (create, edit, delete)
- Course enrollment (assign instructors and students)
- Course progress tracking and completion status

## Screenshots

Include screenshots of the user interface and key features.

## Testing

1. Run automated tests: `python manage.py test`
2. Manually test the application and report any issues or bugs.

## Future Enhancements

- Add user profile pages.
- Implement a notification system.
- Improve the user interface and user experience.

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Make changes and commit them: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin feature-name`
5. Create a pull request.

## Credits

- [Nagi Pragalathan](https://github.com/NagiPragalathan)
- [Contributors](https://github.com/NagiPragalathan/Learning_Management_System_V3/graphs/contributors)

## License

This project is licensed under the MIT License.

## Contact

For questions, feedback, or support, please contact [Nagi Pragalathan](mailto:nagipragalathan@gmail.com).```

# Structure of the Project
Learning_Management_System_V3
├── app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── templates
│   │   ├── app
│   │   │   ├── admin_home.html
│   │   │   ├── all_users.html
│   │   │   ├── edit_user.html
│   │   │   ├── home.html
│   │   │   ├── profile.html
│   │   │   ├── register.html
│   │   │   ├── reset_password.html
│   │   │   ├── view_attendance.html
│   │   │   ├── view_course.html
│   │   │   ├── view_notice.html
│   │   │   ├── view_result.html
│   │   │   └── view_schedule.html
│   │   ├── base.html
│   │   ├── error.html
│   │   ├── not_found.html
│   │   └── registration
│   │       └── register_base.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── lms_v3
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media
├── static
│   ├── css
│   │   ├── login.css
│   │   ├── main.css
│   │   └── register.css
│   ├── images
│   │   └── logo.png
│   └── js
│       ├── jquery.min.js
│       ├── login.js
│       └── register.js
├── templates
│   ├── 403.html
│   ├── 404.html
│   ├── 500.html
│   ├── base.html
│   ├── base_body.html
│   ├── home.html
│   ├── login.html
│   ├── password_reset.html
│   ├── registration
│   │   ├── register_base.html
│   │   ├── register_student.html
│   │   └── register_teacher.html
│   ├── reset_password.html
│   └── verify.html
├── users
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── LICENSE
├── README.md
├── manage.py
└── requirements.txt

