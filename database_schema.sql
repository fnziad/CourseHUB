-- CourseHUB Database Schema
-- University Course Management System

-- Create Database
CREATE DATABASE IF NOT EXISTS university_course_hub;
USE university_course_hub;

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Courses Table
CREATE TABLE IF NOT EXISTS Courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    instructor VARCHAR(100),
    credits INT,
    semester VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Enrollments Table
CREATE TABLE IF NOT EXISTS Enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE,
    UNIQUE KEY unique_enrollment (student_id, course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Resources Table
CREATE TABLE IF NOT EXISTS Resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    link VARCHAR(500) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert Sample Admin User (password: admin123)
-- Note: You should change this password after first login
INSERT INTO Users (username, password, role) VALUES 
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLBK.9.u', 'admin');

-- Insert Comprehensive Sample Courses
INSERT INTO Courses (name, description, instructor, credits, semester) VALUES
('Introduction to Computer Science', 'Explore the fundamentals of programming, algorithms, and computational thinking. Perfect for beginners with no prior experience. Learn Python from scratch and build real-world projects.', 'Dr. Sarah Mitchell', 3, 'Fall 2025'),
('Data Structures and Algorithms', 'Master essential data structures including arrays, linked lists, trees, and graphs. Dive deep into sorting, searching, and optimization algorithms. Prepare for technical interviews at top tech companies.', 'Prof. James Anderson', 4, 'Fall 2025'),
('Database Management Systems', 'Comprehensive coverage of relational databases, SQL, normalization, and transaction management. Hands-on experience with MySQL, PostgreSQL, and NoSQL databases like MongoDB.', 'Dr. Emily Williams', 3, 'Spring 2025'),
('Web Development Fundamentals', 'Build modern, responsive websites from scratch. Learn HTML5, CSS3, JavaScript, and popular frameworks like React and Vue.js. Create a portfolio-worthy project by the end of the course.', 'Prof. Michael Chen', 3, 'Spring 2025'),
('Software Engineering Principles', 'Learn industry-standard practices including Agile development, version control with Git, CI/CD pipelines, testing strategies, and software architecture patterns.', 'Dr. Robert Davis', 4, 'Fall 2025'),
('Machine Learning & AI', 'Introduction to machine learning algorithms, neural networks, and deep learning. Hands-on projects using Python, TensorFlow, and scikit-learn. No advanced math required.', 'Dr. Lisa Thompson', 4, 'Spring 2025'),
('Mobile App Development', 'Create native mobile applications for iOS and Android. Learn React Native, Flutter, and modern mobile design patterns. Build and deploy your own app to app stores.', 'Prof. David Kim', 3, 'Fall 2025'),
('Cybersecurity Essentials', 'Understand security fundamentals, ethical hacking, cryptography, and network security. Learn to identify vulnerabilities and protect systems from cyber threats.', 'Dr. Amanda Foster', 3, 'Spring 2025'),
('Cloud Computing with AWS', 'Master cloud infrastructure with Amazon Web Services. Learn EC2, S3, Lambda, and serverless architecture. Get prepared for AWS certification exams.', 'Prof. Kevin Martinez', 3, 'Fall 2025'),
('Introduction to Data Science', 'Analyze and visualize data using Python, Pandas, and Matplotlib. Learn statistical analysis, data cleaning, and how to extract insights from complex datasets.', 'Dr. Rachel Green', 4, 'Spring 2025'),
('UI/UX Design Principles', 'Master user interface and user experience design. Learn design thinking, wireframing, prototyping with Figma, and usability testing methodologies.', 'Prof. Sophia Lee', 3, 'Fall 2025'),
('Blockchain & Cryptocurrency', 'Understand blockchain technology, smart contracts, and decentralized applications. Learn Solidity programming and build your own cryptocurrency.', 'Dr. Mark Wilson', 3, 'Spring 2025');

-- Insert Comprehensive Sample Resources
INSERT INTO Resources (course_id, name, link) VALUES
-- Introduction to Computer Science
(1, 'Python Official Tutorial', 'https://docs.python.org/3/tutorial/'),
(1, 'CS50 Introduction to Computer Science', 'https://cs50.harvard.edu/'),
(1, 'Automate the Boring Stuff with Python', 'https://automatetheboringstuff.com/'),
(1, 'Python Practice Exercises', 'https://www.practicepython.org/'),

-- Data Structures and Algorithms
(2, 'Introduction to Algorithms (MIT Press)', 'https://mitpress.mit.edu/books/introduction-algorithms'),
(2, 'LeetCode Practice Platform', 'https://leetcode.com/'),
(2, 'VisuAlgo - Algorithm Visualizations', 'https://visualgo.net/'),
(2, 'HackerRank Coding Challenges', 'https://www.hackerrank.com/'),

-- Database Management Systems
(3, 'MySQL Official Documentation', 'https://dev.mysql.com/doc/'),
(3, 'PostgreSQL Tutorial', 'https://www.postgresqltutorial.com/'),
(3, 'MongoDB University', 'https://university.mongodb.com/'),
(3, 'SQL Zoo Interactive Tutorial', 'https://sqlzoo.net/'),

-- Web Development
(4, 'MDN Web Docs', 'https://developer.mozilla.org/'),
(4, 'freeCodeCamp Web Development', 'https://www.freecodecamp.org/'),
(4, 'React Official Documentation', 'https://react.dev/'),
(4, 'CSS-Tricks Complete Guide', 'https://css-tricks.com/'),

-- Software Engineering
(5, 'Git & GitHub Tutorial', 'https://guides.github.com/'),
(5, 'Agile Methodology Guide', 'https://www.atlassian.com/agile'),
(5, 'Clean Code by Robert Martin', 'https://github.com/jnguyen095/clean-code'),
(5, 'Software Design Patterns', 'https://refactoring.guru/design-patterns'),

-- Machine Learning & AI
(6, 'TensorFlow Documentation', 'https://www.tensorflow.org/learn'),
(6, 'Kaggle Learn - ML Courses', 'https://www.kaggle.com/learn'),
(6, 'Andrew Ng ML Course', 'https://www.coursera.org/learn/machine-learning'),
(6, 'Fast.ai Practical Deep Learning', 'https://www.fast.ai/'),

-- Mobile App Development
(7, 'React Native Documentation', 'https://reactnative.dev/'),
(7, 'Flutter Official Docs', 'https://flutter.dev/docs'),
(7, 'iOS Human Interface Guidelines', 'https://developer.apple.com/design/'),
(7, 'Android Developer Guides', 'https://developer.android.com/guide'),

-- Cybersecurity
(8, 'OWASP Top 10 Security Risks', 'https://owasp.org/www-project-top-ten/'),
(8, 'Cybrary Free Security Courses', 'https://www.cybrary.it/'),
(8, 'HackTheBox Practice Platform', 'https://www.hackthebox.com/'),
(8, 'NIST Cybersecurity Framework', 'https://www.nist.gov/cyberframework'),

-- Cloud Computing
(9, 'AWS Free Tier & Tutorials', 'https://aws.amazon.com/free/'),
(9, 'AWS Well-Architected Framework', 'https://aws.amazon.com/architecture/'),
(9, 'Cloud Academy Learning Paths', 'https://cloudacademy.com/'),
(9, 'AWS Certification Guide', 'https://aws.amazon.com/certification/'),

-- Data Science
(10, 'Pandas Documentation', 'https://pandas.pydata.org/docs/'),
(10, 'Data Science Handbook', 'https://jakevdp.github.io/PythonDataScienceHandbook/'),
(10, 'Tableau Public Gallery', 'https://public.tableau.com/'),
(10, 'Google Data Analytics Course', 'https://www.coursera.org/professional-certificates/google-data-analytics'),

-- UI/UX Design
(11, 'Figma Tutorial & Resources', 'https://www.figma.com/resources/learn-design/'),
(11, 'Nielsen Norman Group Articles', 'https://www.nngroup.com/articles/'),
(11, 'Design Systems Repository', 'https://designsystemsrepo.com/'),
(11, 'Laws of UX', 'https://lawsofux.com/'),

-- Blockchain
(12, 'Solidity Documentation', 'https://docs.soliditylang.org/'),
(12, 'Ethereum Development Guides', 'https://ethereum.org/en/developers/'),
(12, 'CryptoZombies Interactive Tutorial', 'https://cryptozombies.io/'),
(12, 'Blockchain Fundamentals Course', 'https://www.coursera.org/learn/blockchain-basics');

-- Reviews Table
CREATE TABLE IF NOT EXISTS Reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_course_review (user_id, course_id)
);

-- Show Tables
SHOW TABLES;

CREATE TABLE IF NOT EXISTS CourseProgress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    progress_percentage INT DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_course_progress (user_id, course_id)
);
