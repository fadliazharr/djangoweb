import unittest
import sqlite3

class TestDatabaseSchemaMigration(unittest.TestCase):
    
    def setUp(self):
        # Connect to an in-memory SQLite database for testing
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        # Initial schema setup
        self.cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        self.connection.commit()

    def test_schema_migration(self):
        # Perform schema migration: Adding a new column 'age' to 'users' table
        self.cursor.execute('ALTER TABLE users ADD COLUMN age INTEGER')
        self.connection.commit()
        
        # Verify the new schema
        self.cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in self.cursor.fetchall()]
        
        self.assertIn('age', columns, "Column 'age' was not added to the 'users' table")
        
        # Test inserting a record with the new schema
        self.cursor.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', 
                            ('Alice', 'alice@example.com', 30))
        self.connection.commit()
        
        # Fetch and verify the inserted record
        self.cursor.execute('SELECT * FROM users WHERE name = ?', ('Alice',))
        user = self.cursor.fetchone()
        
        self.assertIsNotNone(user, "User 'Alice' was not found in the 'users' table")
        self.assertEqual(user[3], 30, "Column 'age' does not have the correct value")

    def tearDown(self):
        self.connection.close()

if __name__ == '__main__':
    unittest.main()
