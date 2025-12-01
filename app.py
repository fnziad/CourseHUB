from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os

# App and Database Initialization
app = Flask(__name__)
app.config.from_object('config.Config')
mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models and User Login Management
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    if user_data:
        return User(id=user_data['id'], username=user_data['username'], role=user_data['role'])
    return None

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # Either 'student' or 'admin'
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
        mysql.connection.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user_data = cur.fetchone()
        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            user = User(id=user_data['id'], username=user_data['username'], role=user_data['role'])
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Student Dashboard
@app.route('/student_dashboard', methods=['GET', 'POST'])
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash("Access denied.", "danger")
        return redirect(url_for('home'))

    cur = mysql.connection.cursor()
    
    # Search functionality
    search_query = request.args.get('search')
    if search_query:
        search_query = f"%{search_query}%"  # For SQL LIKE operator
        cur.execute("SELECT * FROM Courses WHERE name LIKE %s OR description LIKE %s", (search_query, search_query))
    else:
        cur.execute("SELECT * FROM Courses")
    available_courses = cur.fetchall()

    # Enrolled courses
    cur.execute("""
        SELECT Courses.id, Courses.name 
        FROM Enrollments 
        INNER JOIN Courses ON Enrollments.course_id = Courses.id 
        WHERE Enrollments.student_id = %s
    """, (current_user.id,))
    enrolled_courses = cur.fetchall()

    return render_template('student_dashboard.html', available_courses=available_courses, enrolled_courses=enrolled_courses)


@app.route('/api/search_courses', methods=['GET'])
@login_required
def search_courses():
    query = request.args.get('query', '')
    instructor = request.args.get('instructor', '')
    semester = request.args.get('semester', '')
    min_credits = request.args.get('min_credits', type=int)
    max_credits = request.args.get('max_credits', type=int)
    
    cur = mysql.connection.cursor()
    sql = 'SELECT * FROM Courses WHERE 1=1'
    params = []
    
    if query:
        sql += ' AND (name LIKE %s OR description LIKE %s)'
        params.extend([f'%{query}%', f'%{query}%'])
    if instructor:
        sql += ' AND instructor LIKE %s'
        params.append(f'%{instructor}%')
    if semester:
        sql += ' AND semester = %s'
        params.append(semester)
    if min_credits:
        sql += ' AND credits >= %s'
        params.append(min_credits)
    if max_credits:
        sql += ' AND credits <= %s'
        params.append(max_credits)
    
    cur.execute(sql, params)
    courses = cur.fetchall()
    return jsonify(courses)


# Enroll in a Course
@app.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    cur = mysql.connection.cursor()

    # Check if the student is already enrolled in the course
    cur.execute("SELECT * FROM Enrollments WHERE student_id = %s AND course_id = %s", (current_user.id, course_id))
    existing_enrollment = cur.fetchone()

    if existing_enrollment:
        flash("You are already enrolled in this course.", "warning")
    else:
        try:
            # Enroll the student in the course
            cur.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (%s, %s)", (current_user.id, course_id))
            mysql.connection.commit()
            flash("Successfully enrolled in the course!", "success")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
        finally:
            cur.close()

    return redirect(url_for('student_dashboard'))


# Unenroll from a Course
@app.route('/unenroll/<int:course_id>', methods=['POST'])
@login_required
def unenroll(course_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Enrollments WHERE student_id = %s AND course_id = %s", (current_user.id, course_id))
    mysql.connection.commit()
    flash("Successfully unenrolled from the course.", "warning")
    return redirect(url_for('student_dashboard'))

# Admin Dashboard
@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('home'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Courses")
    courses = cur.fetchall()

    # Student enrollment counts for each course
    cur.execute("""
        SELECT Courses.id, Courses.name, COUNT(Enrollments.student_id) AS student_count 
        FROM Courses
        LEFT JOIN Enrollments ON Courses.id = Enrollments.course_id
        GROUP BY Courses.id
    """)
    course_stats = cur.fetchall()

    return render_template('admin_dashboard.html', courses=courses, course_stats=course_stats)

# Add a Course (Admin Only)
@app.route('/admin/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if current_user.role != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        instructor = request.form['instructor']
        credits = request.form['credits']
        semester = request.form['semester']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Courses (name, description, instructor, credits, semester)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, description, instructor, credits, semester))
        mysql.connection.commit()
        flash("Course added successfully!", "success")
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_add_course.html')

# Delete a Course (Admin Only)
@app.route('/admin/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    if current_user.role != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('dashboard'))
    
    cur = mysql.connection.cursor()
    try:
        # First, delete all enrollments associated with the course
        cur.execute("DELETE FROM Enrollments WHERE course_id = %s", (course_id,))
        mysql.connection.commit()

        # Then, delete the course
        cur.execute("DELETE FROM Courses WHERE id = %s", (course_id,))
        mysql.connection.commit()
        flash("Course deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
    finally:
        cur.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/upload_resource/<int:course_id>', methods=['GET', 'POST'])
@login_required
def upload_resource(course_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM Courses WHERE id = %s", (course_id,))
    course_name = cur.fetchone()

    if request.method == 'POST':
        resource_name = request.form['resource_name']
        resource_link = request.form['resource_link']
        cur.execute(
            "INSERT INTO Resources (course_id, name, link, upload_date) VALUES (%s, %s, %s, NOW())",
            (course_id, resource_name, resource_link)
        )
        mysql.connection.commit()
        flash("Resource link added successfully!", "success")
        return redirect(url_for('upload_resource', course_id=course_id))
    
    cur.execute("SELECT * FROM Resources WHERE course_id = %s", (course_id,))
    resources = cur.fetchall()
    return render_template('admin_upload_resource.html', course_id=course_id, course_name=course_name[0], resources=resources)



# Edit a Course (Admin Only)
@app.route('/admin/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    if current_user.role != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('admin_dashboard'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Get updated course details from the form
        name = request.form['name']
        description = request.form['description']
        instructor = request.form['instructor']
        credits = request.form['credits']
        semester = request.form['semester']

        # Update the course in the database
        try:
            cur.execute("""
                UPDATE Courses 
                SET name = %s, description = %s, instructor = %s, credits = %s, semester = %s 
                WHERE id = %s
            """, (name, description, instructor, credits, semester, course_id))
            mysql.connection.commit()
            flash("Course updated successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
        finally:
            cur.close()

        return redirect(url_for('admin_dashboard'))

    # Fetch the course details to pre-fill the form
    cur.execute("SELECT * FROM Courses WHERE id = %s", (course_id,))
    course = cur.fetchone()
    if not course:
        flash("Course not found.", "danger")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_edit_course.html', course=course)


# View Resources (Student/Admin)

@app.route('/resources/<int:course_id>')
@login_required
def view_resources(course_id):
    cur = mysql.connection.cursor()
    
    # Fetch course name
    cur.execute("SELECT name FROM Courses WHERE id = %s", (course_id,))
    course = cur.fetchone()
    if not course:
        flash("Course not found!", "danger")
        return redirect(url_for('dashboard' if current_user.role == 'student' else 'admin_dashboard'))
    course_name = course[0]

    # Fetch resources for the course
    cur.execute("SELECT * FROM Resources WHERE course_id = %s", (course_id,))
    resources = cur.fetchall()

    # Determine the correct "Back to Dashboard" URL based on user role
    back_to_dashboard = '/student_dashboard' if current_user.role == 'student' else '/admin_dashboard'

    return render_template(
        'view_resources.html', 
        course_name=course_name, 
        resources=resources, 
        back_to_dashboard=back_to_dashboard
    )

# Delete a Resource (Admin Only)
@app.route('/admin/delete_resource/<int:resource_id>/<int:course_id>', methods=['POST'])
@login_required
def delete_resource(resource_id, course_id):
    if current_user.role != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('admin_dashboard'))
    
    cur = mysql.connection.cursor()
    try:
        # Delete the resource by ID
        cur.execute("DELETE FROM resources WHERE id = %s", (resource_id,))
        mysql.connection.commit()
        flash("Resource deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while deleting the resource: {str(e)}", "danger")
    finally:
        cur.close()

    # Redirect back to the resource management page for the same course
    return redirect(url_for('upload_resource', course_id=course_id))


if __name__ == '__main__':
    app.run(debug=True)
