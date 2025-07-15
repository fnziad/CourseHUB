# CourseHUB - University Course Management System

A comprehensive web-based course management system built with Flask that allows students to enroll in courses and access resources, while providing administrators with tools to manage courses and upload educational materials.

## Features

### For Students

- **User Registration & Authentication**: Secure account creation and login system
- **Course Browsing**: View all available courses with descriptions and instructor information
- **Course Search**: Search for courses by name or description
- **Course Enrollment**: Enroll in and unenroll from courses
- **Resource Access**: Access course materials and resources uploaded by instructors
- **Personal Dashboard**: View enrolled courses and manage course participation

### For Administrators

- **Course Management**: Add, edit, and delete courses
- **Resource Management**: Upload and manage course resources (links, materials)
- **Student Analytics**: View enrollment statistics for each course
- **Admin Dashboard**: Comprehensive overview of all courses and student enrollments

### General Features

- **Dark/Light Mode**: Toggle between light and dark themes
- **Responsive Design**: Mobile-friendly interface
- **Flash Messages**: Real-time feedback for user actions
- **Secure Authentication**: Password hashing and session management

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: MySQL
- **Authentication**: Flask-Login, Flask-Bcrypt
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with Google Fonts (Poppins)
- **Database ORM**: Flask-MySQLdb

## Installation

### Prerequisites

- Python 3.7+
- MySQL Server
- XAMPP (optional, for local MySQL setup)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/fnziad/CourseHUB.git
   cd CourseHUB
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install flask flask-mysqldb flask-bcrypt flask-login
   ```

4. **Database Setup**

   - Start MySQL server (via XAMPP or standalone)
   - Create a database named `university_course_hub`
   - Create the required tables:

   ```sql
   CREATE DATABASE university_course_hub;
   USE university_course_hub;

   CREATE TABLE Users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
       role ENUM('student', 'admin') NOT NULL
   );

   CREATE TABLE Courses (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       description TEXT,
       instructor VARCHAR(100),
       credits INT,
       semester VARCHAR(20)
   );

   CREATE TABLE Enrollments (
       id INT AUTO_INCREMENT PRIMARY KEY,
       student_id INT,
       course_id INT,
       enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (student_id) REFERENCES Users(id),
       FOREIGN KEY (course_id) REFERENCES Courses(id)
   );

   CREATE TABLE Resources (
       id INT AUTO_INCREMENT PRIMARY KEY,
       course_id INT,
       name VARCHAR(100) NOT NULL,
       link VARCHAR(255) NOT NULL,
       upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (course_id) REFERENCES Courses(id)
   );
   ```

5. **Configure database connection**

   - Update `config.py` with your MySQL connection details:

   ```python
   class Config:
       SECRET_KEY = 'your_secret_key_here'
       MYSQL_HOST = '127.0.0.1'
       MYSQL_PORT = 3306
       MYSQL_USER = 'your_mysql_username'
       MYSQL_PASSWORD = 'your_mysql_password'
       MYSQL_DB = 'university_course_hub'
   ```

6. **Run the application**

   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and go to `http://localhost:5000`

## Usage

### First Time Setup

1. Register as an admin user to manage courses
2. Register as a student to enroll in courses
3. Log in with your credentials

### Student Workflow

1. Register for a student account
2. Browse available courses
3. Use the search functionality to find specific courses
4. Enroll in desired courses
5. Access course resources from your dashboard

### Admin Workflow

1. Register for an admin account
2. Add new courses with details (name, description, instructor, credits, semester)
3. Upload resources for each course
4. Edit or delete courses as needed
5. Monitor student enrollments

## Project Structure

```
CourseHUB/
├── app.py                 # Main Flask application
├── app_demo.py           # Demo version (no database required)
├── config.py             # Database configuration
├── README.md             # Project documentation
├── static/
│   └── css/
│       └── styles.css    # Custom styles with dark/light mode
├── templates/
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── student_dashboard.html    # Student dashboard
│   ├── admin_dashboard.html      # Admin dashboard
│   ├── admin_add_course.html     # Add course form
│   ├── admin_edit_course.html    # Edit course form
│   ├── admin_upload_resource.html # Resource management
│   └── view_resources.html       # Resource viewing
└── __pycache__/          # Python cache files
```

## Demo Mode

For testing without database setup, use the demo version:

```bash
python app_demo.py
```

This runs on port 5001 and uses mock data instead of a MySQL database.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Security Notes

- Change the `SECRET_KEY` in `config.py` for production use
- Use environment variables for sensitive configuration
- Implement proper input validation and sanitization
- Use HTTPS in production
- Regularly update dependencies

## Future Enhancements

- File upload functionality for course materials
- Email notifications for course enrollment
- Grade management system
- Course calendar integration
- Advanced search filters
- User profile management
- Course ratings and reviews

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact:

- Email: fahad.nadim.ziad@g.bracu.ac.bd
- GitHub: [fnziad](https://github.com/fnziad)

---

© 2025 CourseHUB - All Rights Reserved
