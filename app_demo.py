from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os

# App Initialization (without MySQL for demo)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo_secret_key'

# Mock data for demo
mock_courses = [
    {'id': 1, 'name': 'Computer Science 101', 'description': 'Introduction to Computer Science'},
    {'id': 2, 'name': 'Mathematics 201', 'description': 'Advanced Mathematics'},
    {'id': 3, 'name': 'Physics 301', 'description': 'Quantum Physics'}
]

mock_resources = [
    {'id': 1, 'course_id': 1, 'title': 'Python Programming Guide', 'url': 'https://python.org', 'description': 'Learn Python basics'},
    {'id': 2, 'course_id': 1, 'title': 'Data Structures', 'url': 'https://example.com/ds', 'description': 'Data structures tutorial'},
    {'id': 3, 'course_id': 2, 'title': 'Calculus Reference', 'url': 'https://example.com/calc', 'description': 'Calculus reference guide'}
]

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Register Route (Demo)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash('Registration successful! (Demo mode - no database)', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login Route (Demo)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role', 'student')
        session['user_id'] = 1
        session['username'] = username
        session['role'] = role
        flash('Login successful! (Demo mode)', 'success')
        
        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Student Dashboard
@app.route('/student/dashboard')
def student_dashboard():
    return render_template('student_dashboard.html', courses=mock_courses)

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html', courses=mock_courses)

# View Resources
@app.route('/resources/<int:course_id>')
def view_resources(course_id):
    course = next((c for c in mock_courses if c['id'] == course_id), None)
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('home'))
    
    course_resources = [r for r in mock_resources if r['course_id'] == course_id]
    # Format resources to match template expectations [id, course_id, title, url, description]
    formatted_resources = [[r['id'], r['course_id'], r['title'], r['url'], r['description']] for r in course_resources]
    
    return render_template('view_resources.html', 
                         course_name=course['name'], 
                         resources=formatted_resources,
                         back_to_dashboard=url_for('student_dashboard'))

# Admin routes (simplified for demo)
@app.route('/admin/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        flash('Course added successfully! (Demo mode)', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_add_course.html')

@app.route('/admin/upload_resource/<int:course_id>', methods=['GET', 'POST'])
def upload_resource(course_id):
    course = next((c for c in mock_courses if c['id'] == course_id), None)
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        flash('Resource uploaded successfully! (Demo mode)', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_upload_resource.html', course=course)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
