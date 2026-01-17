
import sqlite3
import csv
import os
from datetime import datetime
import re

class CSVDatabaseImporter:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def create_database(self):
        """Create SQLite database and users table"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                age INTEGER,
                city TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        print(f"✓ Database '{self.db_name}' created successfully")
    
    def create_sample_csv(self, filename='users.csv'):
        """Create a sample CSV file for demonstration"""
        sample_data = [
            ['name', 'email', 'phone', 'age', 'city'],
            ['John Doe', 'john.doe@example.com', '+1-555-0101', '28', 'New York'],
            ['Jane Smith', 'jane.smith@example.com', '+1-555-0102', '34', 'Los Angeles'],
            ['Bob Johnson', 'bob.j@example.com', '+1-555-0103', '45', 'Chicago'],
            ['Alice Williams', 'alice.w@example.com', '+1-555-0104', '29', 'Houston'],
            ['Charlie Brown', 'charlie.b@example.com', '+1-555-0105', '52', 'Phoenix'],
            ['Diana Prince', 'diana.p@example.com', '+1-555-0106', '31', 'Philadelphia'],
            ['Eve Davis', 'eve.d@example.com', '+1-555-0107', '26', 'San Antonio'],
            ['Frank Miller', 'frank.m@example.com', '+1-555-0108', '38', 'San Diego'],
            ['Grace Lee', 'grace.l@example.com', '+1-555-0109', '42', 'Dallas'],
            ['Henry Wilson', 'henry.w@example.com', '+1-555-0110', '33', 'San Jose']
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
        
        print(f"✓ Sample CSV file '{filename}' created")
        return filename
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def read_csv(self, filename):
        """Read data from CSV file with validation"""
        if not os.path.exists(filename):
            print(f"✗ File '{filename}' not found")
            return []
        
        users = []
        errors = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                
                for row_num, row in enumerate(csv_reader, start=2):
                    # Validate required fields
                    if not row.get('name') or not row.get('email'):
                        errors.append(f"Row {row_num}: Missing required fields")
                        continue
                    
                    # Validate email
                    if not self.validate_email(row['email']):
                        errors.append(f"Row {row_num}: Invalid email format")
                        continue
                    
                    # Validate age if present
                    age = None
                    if row.get('age'):
                        try:
                            age = int(row['age'])
                            if age < 0 or age > 120:
                                errors.append(f"Row {row_num}: Invalid age value")
                                continue
                        except ValueError:
                            errors.append(f"Row {row_num}: Age must be a number")
                            continue
                    
                    user = {
                        'name': row['name'].strip(),
                        'email': row['email'].strip().lower(),
                        'phone': row.get('phone', '').strip(),
                        'age': age,
                        'city': row.get('city', '').strip()
                    }
                    users.append(user)
            
            print(f"✓ Read {len(users)} valid records from CSV")
            
            if errors:
                print(f"\n⚠ {len(errors)} validation errors:")
                for error in errors[:5]:  # Show first 5 errors
                    print(f"  - {error}")
                if len(errors) > 5:
                    print(f"  ... and {len(errors) - 5} more")
            
            return users
            
        except Exception as e:
            print(f"✗ Error reading CSV: {e}")
            return []
    
    def import_users(self, users):
        """Import users into database with duplicate handling"""
        if not users:
            print("No users to import")
            return
        
        inserted = 0
        duplicates = 0
        
        for user in users:
            try:
                self.cursor.execute('''
                    INSERT INTO users (name, email, phone, age, city)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user['name'], user['email'], user['phone'], 
                      user['age'], user['city']))
                inserted += 1
                
            except sqlite3.IntegrityError:
                # Email already exists
                duplicates += 1
                print(f"  ⚠ Duplicate email: {user['email']}")
        
        self.conn.commit()
        
        print(f"\n✓ Successfully inserted {inserted} users")
        if duplicates > 0:
            print(f"  ⚠ Skipped {duplicates} duplicate entries")
    
    def display_users(self, limit=None):
        """Display all users from database"""
        query = 'SELECT * FROM users ORDER BY created_at DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        
        print("\n" + "="*80)
        print(f"USERS IN DATABASE (Total: {len(users)})")
        print("="*80)
        
        if not users:
            print("No users found")
        else:
            for user in users:
                print(f"\nID: {user[0]}")
                print(f"Name: {user[1]}")
                print(f"Email: {user[2]}")
                print(f"Phone: {user[3] if user[3] else 'N/A'}")
                print(f"Age: {user[4] if user[4] else 'N/A'}")
                print(f"City: {user[5] if user[5] else 'N/A'}")
                print(f"Created: {user[6]}")
                print("-" * 80)
    
    def get_statistics(self):
        """Get database statistics"""
        self.cursor.execute('SELECT COUNT(*) FROM users')
        total = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT AVG(age) FROM users WHERE age IS NOT NULL')
        avg_age = self.cursor.fetchone()[0]
        
        self.cursor.execute('''
            SELECT city, COUNT(*) as count 
            FROM users 
            WHERE city IS NOT NULL AND city != ''
            GROUP BY city 
            ORDER BY count DESC 
            LIMIT 5
        ''')
        top_cities = self.cursor.fetchall()
        
        print("\n" + "="*80)
        print("DATABASE STATISTICS")
        print("="*80)
        print(f"Total Users: {total}")
        if avg_age:
            print(f"Average Age: {avg_age:.1f}")
        
        if top_cities:
            print("\nTop Cities:")
            for city, count in top_cities:
                print(f"  - {city}: {count} users")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("\n✓ Database connection closed")

def main():
    """Main execution function"""
    importer = CSVDatabaseImporter()
    
    try:
        print("CSV to Database Import Tool")
        print("="*80)
        
        # Step 1: Create database
        importer.create_database()
        
        # Step 2: Create sample CSV (or use existing)
        csv_file = 'users.csv'
        if not os.path.exists(csv_file):
            csv_file = importer.create_sample_csv()
        else:
            print(f"✓ Using existing CSV file '{csv_file}'")
        
        # Step 3: Read CSV data
        users = importer.read_csv(csv_file)
        
        # Step 4: Import to database
        importer.import_users(users)
        
        # Step 5: Display results
        importer.display_users(limit=10)
        
        # Step 6: Show statistics
        importer.get_statistics()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        importer.close()

if __name__ == "__main__":
    main()