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
- Improve the user interface and user experience .

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
<br>├── app
<br>│   ├── __init__.py
<br>│   ├── admin.py
<br>│   ├── apps.py
<br>│   ├── models.py
<br>│   ├── templates
<br>│   │   ├── app
<br>│   │   │   ├── admin_home.html
<br>│   │   │   ├── all_users.html
<br>│   │   │   ├── edit_user.html
<br>│   │   │   ├── home.html
<br>│   │   │   ├── profile.html
<br>│   │   │   ├── register.html
<br>│   │   │   ├── reset_password.html
<br>│   │   │   ├── view_attendance.html
<br>│   │   │   ├── view_course.html
<br>│   │   │   ├── view_notice.html
<br>│   │   │   ├── view_result.html
<br>│   │   │   └── view_schedule.html
<br>│   │   ├── base.html
<br>│   │   ├── error.html
<br>│   │   ├── not_found.html
<br>│   │   └── registration
<br>│   │       └── register_base.html
<br>│   ├── tests.py
<br>│   ├── urls.py
<br>│   └── views.py
<br>├── lms_v3
<br>│   ├── __init__.py
<br>│   ├── asgi.py
<br>│   ├── settings.py
<br>│   ├── urls.py
<br>│   └── wsgi.py
<br>├── media
<br>├── static
<br>│   ├── css
<br>│   │   ├── login.css
<br>│   │   ├── main.css
<br>│   │   └── register.css
<br>│   ├── images
<br>│   │   └── logo.png
<br>│   └── js
<br>│       ├── jquery.min.js
<br>│       ├── login.js
<br>│       └── register.js
<br>├── templates
<br>│   ├── 403.html
<br>│   ├── 404.html
<br>│   ├── 500.html
<br>│   ├── base.html
<br>│   ├── base_body.html
<br>│   ├── home.html
<br>│   ├── login.html
<br>│   ├── password_reset.html
<br>│   ├── registration
<br>│   │   ├── register_base.html
<br>│   │   ├── register_student.html
<br>│   │   └── register_teacher.html
<br>│   ├── reset_password.html
<br>│   └── verify.html
<br>├── users
<br>│   ├── __init__.py
<br>│   ├── admin.py
<br>│   ├── apps.py
<br>│   ├── forms.py
<br>│   ├── models.py
<br>│   ├── signals.py
<br>│   ├── tests.py
<br>│   ├── urls.py
<br>│   └── views.py
<br>├── db.sqlite3
<br>├── LICENSE
<br>├── README.md
<br>├── manage.py
<br>└── requirements.txt
