#!/bin/bash

# CourseHUB Startup Script

echo "🚀 Starting CourseHUB..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your database credentials before running again."
    exit 1
fi

# Install/update dependencies
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt

# Check if database exists
echo "🗄️  Checking database connection..."
python3 -c "
import os
from dotenv import load_dotenv
import MySQLdb

load_dotenv()
try:
    conn = MySQLdb.connect(
        host=os.getenv('MYSQL_HOST', '127.0.0.1'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        port=int(os.getenv('MYSQL_PORT', 3306))
    )
    cursor = conn.cursor()
    cursor.execute('SHOW DATABASES LIKE \"university_course_hub\"')
    if not cursor.fetchone():
        print('⚠️  Database not found! Run: mysql -u root -p < database_schema.sql')
        exit(1)
    print('✅ Database connected successfully!')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    print('Please check your MySQL server and .env configuration')
    exit(1)
"

if [ $? -ne 0 ]; then
    exit 1
fi

# Start the application
echo ""
echo "✅ All checks passed!"
echo "🌐 Starting Flask application..."
echo "📍 Access at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
