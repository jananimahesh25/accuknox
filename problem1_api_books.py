
import sqlite3
import requests
import json
from datetime import datetime

class BookAPIHandler:
    def __init__(self, db_name='books.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def create_database(self):
        """Create SQLite database and books table"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publication_year INTEGER,
                isbn TEXT,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        print(f"✓ Database '{self.db_name}' created successfully")
        
    def fetch_books_from_api(self):
        """
        Fetch books from Google Books API
        Using public API that doesn't require authentication
        """
        try:
            # Using Google Books API as example
            api_url = "https://www.googleapis.com/books/v1/volumes"
            params = {
                'q': 'python programming',
                'maxResults': 10
            }
            
            print("Fetching data from API...")
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            books = []
            
            if 'items' in data:
                for item in data['items']:
                    volume_info = item.get('volumeInfo', {})
                    book = {
                        'title': volume_info.get('title', 'N/A'),
                        'author': ', '.join(volume_info.get('authors', ['Unknown'])),
                        'publication_year': self._extract_year(volume_info.get('publishedDate', '')),
                        'isbn': self._extract_isbn(volume_info.get('industryIdentifiers', []))
                    }
                    books.append(book)
                    
            print(f"✓ Fetched {len(books)} books from API")
            return books
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching data from API: {e}")
            return []
    
    def _extract_year(self, date_string):
        """Extract year from date string"""
        if not date_string:
            return None
        try:
            return int(date_string[:4])
        except (ValueError, IndexError):
            return None
    
    def _extract_isbn(self, identifiers):
        """Extract ISBN from identifiers list"""
        for identifier in identifiers:
            if identifier.get('type') == 'ISBN_13':
                return identifier.get('identifier')
        return None
    
    def store_books(self, books):
        """Store books in SQLite database"""
        if not books:
            print("No books to store")
            return
        
        for book in books:
            self.cursor.execute('''
                INSERT INTO books (title, author, publication_year, isbn)
                VALUES (?, ?, ?, ?)
            ''', (book['title'], book['author'], book['publication_year'], book['isbn']))
        
        self.conn.commit()
        print(f"✓ Stored {len(books)} books in database")
    
    def display_books(self):
        """Retrieve and display all books from database"""
        self.cursor.execute('SELECT * FROM books ORDER BY publication_year DESC')
        books = self.cursor.fetchall()
        
        print("\n" + "="*80)
        print("BOOKS IN DATABASE")
        print("="*80)
        
        if not books:
            print("No books found in database")
        else:
            for book in books:
                print(f"\nID: {book[0]}")
                print(f"Title: {book[1]}")
                print(f"Author: {book[2]}")
                print(f"Year: {book[3] if book[3] else 'N/A'}")
                print(f"ISBN: {book[4] if book[4] else 'N/A'}")
                print(f"Fetched: {book[5]}")
                print("-" * 80)
        
        return books
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("\n✓ Database connection closed")

def main():
    """Main execution function"""
    handler = BookAPIHandler()
    
    try:
        # Step 1: Create database
        handler.create_database()
        
        # Step 2: Fetch data from API
        books = handler.fetch_books_from_api()
        
        # Step 3: Store in database
        handler.store_books(books)
        
        # Step 4: Display data
        handler.display_books()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        handler.close()

if __name__ == "__main__":
    main()