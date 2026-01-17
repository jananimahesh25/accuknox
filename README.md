# AI/ML Trainee Assignment - Complete Solutions



## AccuKnox Position Submission
---



## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Problem 1: API Data Retrieval and Storage](#problem-1)
4. [Problem 2: Data Processing and Visualization](#problem-2)
5. [Problem 3: CSV Import to Database](#problem-3)
6. [Assignment 2: Theoretical Questions](#assignment-2)
7. [Project Structure](#project-structure)
8. [Troubleshooting](#troubleshooting)

---



## 🔧 Prerequisites



### Required Software:
- **Python 3.8+** (Download from [python.org](https://www.python.org/downloads/))
- **pip** (Python package installer - comes with Python)
- **Git** (Optional, for version control)



### Check Your Installation:
```bash
python --version  # Should show Python 3.8 or higher
pip --version     # Should show pip version
```

---



## 📦 Installation



### Step 1: Create Project Directory
```bash



# Create and navigate to project folder
mkdir accuknox_assignment
cd accuknox_assignment
```



### Step 2: Create Virtual Environment (Recommended)
```bash



# Windows
python -m venv venv
venv\Scripts\activate



# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```



### Step 3: Install Required Libraries
```bash
pip install requests matplotlib pandas sqlite3
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
requests==2.31.0
matplotlib==3.8.0
pandas==2.1.0
```

---



## 📚 Problem 1: API Data Retrieval and Storage



### Overview
Fetches book data from Google Books API, stores it in SQLite database, and displays results.



### Files Needed
- `problem1_api_books.py`



### Step-by-Step Instructions:
#### 1. Create the Python File
Save the Problem 1 code as `problem1_api_books.py`

#### 2. Run the Script
```bash
python problem1_api_books.py
```

#### 3. Expected Output
```
✓ Database 'books.db' created successfully
Fetching data from API...
✓ Fetched 10 books from API
✓ Stored 10 books in database

================================================================================
BOOKS IN DATABASE
================================================================================

ID: 1
Title: Python Programming for Beginners
Author: John Smith
Year: 2023
ISBN: 9781234567890
Fetched: 2026-01-17 10:30:45
--------------------------------------------------------------------------------
...
✓ Database connection closed
```

#### 4. Verify Database
```bash



# Windows
sqlite3 books.db



# macOS/Linux
sqlite3 books.db



# Inside SQLite shell:
.tables          # Should show 'books' table
SELECT * FROM books LIMIT 5;
.quit
```



### Key Features:
- ✅ Fetches real data from Google Books API
- ✅ Validates and cleans data before storage
- ✅ Handles errors gracefully
- ✅ Creates SQLite database automatically
- ✅ Prevents duplicate entries



### Customization Options:
**Change Search Query:**
```python



# In fetch_books_from_api() method, modify:
params = {
    'q': 'artificial intelligence',  # Change this
    'maxResults': 20                  # Or increase results
}
```

**Add More Fields:**
```python



# Modify the database schema in create_database():
self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        publication_year INTEGER,
        isbn TEXT,
        description TEXT,        # Add this
        page_count INTEGER,      # Add this
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
```

---



## 📊 Problem 2: Data Processing and Visualization



### Overview
Generates student test score data, calculates statistics, and creates comprehensive visualizations.



### Files Needed
- `problem2_visualization.py`



### Step-by-Step Instructions:
#### 1. Create the Python File
Save the Problem 2 code as `problem2_visualization.py`

#### 2. Run the Script
```bash
python problem2_visualization.py
```

#### 3. Expected Output
```
Starting Student Score Analysis...
--------------------------------------------------------------------------------
✓ Fetched data for 20 students

================================================================================
STUDENT SCORE STATISTICS
================================================================================

Math:
  Average: 82.45
  Median: 83.00
  Std Dev: 10.23
  Range: 60 - 100

Science:
  Average: 78.90
  Median: 79.50
  Std Dev: 11.45
  Range: 61 - 98
...

✓ Visualization saved as 'student_scores_analysis.png'
✓ Results exported to 'student_analysis_results.json'

================================================================================
Analysis Complete!
================================================================================
```

#### 4. Output Files Generated
- `student_scores_analysis.png` - Comprehensive visualization with 4 charts
- `student_analysis_results.json` - Raw data and statistics in JSON format



### Generated Visualizations Include:
1. **Average Scores Bar Chart** - Shows mean scores per subject
2. **Average vs Median Comparison** - Identifies score distribution skewness
3. **Standard Deviation Chart** - Shows score variability
4. **Box Plot Distribution** - Shows quartiles, outliers, and spread



### Customization Options:
**Modify Number of Students:**
```python



# In _generate_mock_data() method:
for i in range(50):  # Change from 20 to 50
```

**Add More Subjects:**
```python
subjects = ['Math', 'Science', 'English', 'History', 'Geography', 
            'Physics', 'Chemistry', 'Biology']  # Add subjects
```

**Use Real API Data:**
```python
def fetch_student_data(self):
    """Fetch from actual API"""
    response = requests.get('https://your-api.com/students')
    data = response.json()
    # Process and return data
```

**Change Visualization Colors:**
```python



# Modify color parameters in create_visualizations():
bars1 = ax1.bar(subjects, averages, color='darkblue', alpha=0.9)
```

---



## 💾 Problem 3: CSV Import to Database



### Overview
Reads user data from CSV file, validates it, and imports into SQLite database.



### Files Needed
- `problem3_csv_import.py`



### Step-by-Step Instructions:
#### 1. Create the Python File
Save the Problem 3 code as `problem3_csv_import.py`

#### 2. Run the Script
```bash
python problem3_csv_import.py
```

#### 3. Expected Output
```
CSV to Database Import Tool
================================================================================
✓ Database 'users.db' created successfully
✓ Sample CSV file 'users.csv' created
✓ Read 10 valid records from CSV

✓ Successfully inserted 10 users

================================================================================
USERS IN DATABASE (Total: 10)
================================================================================

ID: 1
Name: John Doe
Email: john.doe@example.com
Phone: +1-555-0101
Age: 28
City: New York
Created: 2026-01-17 10:35:22
--------------------------------------------------------------------------------
...

================================================================================
DATABASE STATISTICS
================================================================================
Total Users: 10
Average Age: 35.8

Top Cities:
  - New York: 1 users
  - Los Angeles: 1 users
  - Chicago: 1 users

✓ Database connection closed
```

#### 4. Verify Generated Files
```bash
ls -la



# Should show:



# users.csv - Sample CSV file



# users.db  - SQLite database
```



### Features:
- ✅ Automatic sample CSV generation
- ✅ Email validation using regex
- ✅ Age validation (0-120 range)
- ✅ Duplicate detection and handling
- ✅ Error reporting for invalid records
- ✅ Database statistics and analytics



### Using Your Own CSV File:
#### CSV Format Required:
```csv
name,email,phone,age,city
John Doe,john@example.com,+1-555-0101,28,New York
Jane Smith,jane@example.com,+1-555-0102,34,Los Angeles
```

#### Place Your CSV:
```bash



# Save your CSV as 'users.csv' in the same directory



# Then run:
python problem3_csv_import.py
```



### Validation Rules:
1. **Required Fields**: name, email
2. **Email Format**: Must match standard email pattern
3. **Age**: Must be integer between 0-120
4. **Duplicates**: Same email will be skipped



### Handling Errors:
**If you get validation errors:**
```
⚠ 2 validation errors:
  - Row 3: Invalid email format
  - Row 5: Age must be a number
```

**Fix in your CSV file and rerun the script.**

---



## 📝 Assignment 2: Theoretical Questions
All theoretical answers are provided in the `assignment2_answers.md` file, including:



### Question 1: Self-Assessment
Detailed ratings on LLM, Deep Learning, AI, and ML with justifications.



### Question 2: LLM Chatbot Architecture
- Complete architectural diagram
- Component descriptions
- Implementation phases
- Technology recommendations



### Question 3: Vector Databases
- Comprehensive explanation of vector databases
- Comparison of popular options
- Hypothetical problem: Medical Research Assistant
- Detailed justification for choosing Weaviate

---



## 📁 Project Structure
```
accuknox_assignment/
│
├── problem1_api_books.py          # Problem 1 solution
├── problem2_visualization.py      # Problem 2 solution
├── problem3_csv_import.py         # Problem 3 solution
├── assignment2_answers.md         # Theoretical answers
│
├── requirements.txt               # Python dependencies
├── README.md                      # This file
│
├── books.db                       # Generated by Problem 1
├── users.db                       # Generated by Problem 3
├── users.csv                      # Generated by Problem 3
│
├── student_scores_analysis.png    # Generated by Problem 2
└── student_analysis_results.json  # Generated by Problem 2
```

---



## 🐛 Troubleshooting



### Common Issues and Solutions:
#### 1. ModuleNotFoundError: No module named 'requests'
**Solution:**
```bash
pip install requests
```

#### 2. API Request Timeout
**Solution:**
```python



# Increase timeout in fetch_books_from_api():
response = requests.get(api_url, params=params, timeout=30)
```

#### 3. SQLite Database Locked
**Solution:**
```bash



# Close any SQLite connections



# Delete the .db file and rerun
rm books.db users.db
python problem1_api_books.py
```

#### 4. Matplotlib Display Issues (Linux)
**Solution:**
```bash



# Install tkinter
sudo apt-get install python3-tk
```

#### 5. Permission Denied on File Creation
**Solution:**
```bash



# Run with appropriate permissions
chmod +w .
```

#### 6. CSV Encoding Issues
**Solution:**
```python



# If you have special characters, ensure UTF-8:
with open(filename, 'r', encoding='utf-8-sig') as f:
```

---



## 🎯 Testing the Solutions



### Quick Test All Scripts:
```bash



# Test Problem 1
python problem1_api_books.py



# Test Problem 2
python problem2_visualization.py



# Test Problem 3
python problem3_csv_import.py
```



### Verify Outputs:
```bash



# Check databases
ls *.db



# Check visualizations
ls *.png



# Check data files
ls *.json *.csv
```

---



## 📧 Submission Checklist
Before submitting, ensure you have:

- [ ] All three Python scripts (Problem 1, 2, 3)
- [ ] Assignment 2 theoretical answers document
- [ ] README.md with instructions
- [ ] requirements.txt file
- [ ] Latest resume attached
- [ ] All code properly commented
- [ ] No ChatGPT-generated code (as per requirements)
- [ ] All assumptions documented



### Submission Format:
**Option 1: Google Drive Link**
- Create a folder with all files
- Share with "Anyone with the link can view"
- Include link in email

**Option 2: Document/PDF**
- Save as: `[YourName]_AccuKnox_Assignment.pdf`
- Include all code and answers
- Attach latest resume

---



## 🚀 Advanced Enhancements (Optional)
If you want to go beyond the requirements:



### 1. Add Unit Tests
```python



# test_problem1.py
import unittest
from problem1_api_books import BookAPIHandler

class TestBookAPI(unittest.TestCase):
    def test_database_creation(self):
        handler = BookAPIHandler('test.db')
        handler.create_database()
        self.assertTrue(os.path.exists('test.db'))
```



### 2. Add Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```



### 3. Create Web Interface
```python



# Using Flask
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/books')
def show_books():
    # Connect to database and fetch books
    return render_template('books.html', books=books)
```

---



## 📚 Additional Resources
- **Python Documentation**: https://docs.python.org/3/
- **SQLite Tutorial**: https://www.sqlitetutorial.net/
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/
- **Requests Library**: https://requests.readthedocs.io/
- **Vector Databases**: https://www.pinecone.io/learn/vector-database/

---



## ✅ Final Notes
1. **Code Quality**: All code follows PEP 8 style guidelines
2. **Error Handling**: Comprehensive try-catch blocks included
3. **Documentation**: Inline comments and docstrings provided
4. **Scalability**: Code designed for easy modification and extension
5. **Best Practices**: Object-oriented design, modular functions

**Good luck with your interview!** 🎉

---

**Prepared by**: [Your Name]  
**Date**: January 17, 2026  
**Position**: AI/ML Trainee at AccuKnox