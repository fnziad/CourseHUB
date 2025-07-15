class Config:
    SECRET_KEY = 'your_secret_key'
    MYSQL_HOST = '127.0.0.1'  # Use 127.0.0.1 instead of localhost to avoid socket issues
    MYSQL_PORT = 3306         # Replace with the port MySQL is running on (e.g., 3307 if XAMPP uses a custom port)
    MYSQL_USER = 'root'       # Default XAMPP username
    MYSQL_PASSWORD = ''       # Default XAMPP password (empty if no password)
    MYSQL_DB = 'university_course_hub'
