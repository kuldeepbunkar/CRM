import sqlite3
import logging

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('data/crm.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('PRAGMA foreign_keys = ON')
            self.setup_tables()
        except Exception as e:
            logging.critical(f"Failed to initialize database: {str(e)}")
            raise
    
    def setup_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP
            )
        ''')
        # Add other table creation queries

        # Leads table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                source TEXT,
                interest_type TEXT,
                status TEXT,
                created_at TIMESTAMP,
                interested_property_id INTEGER,
                FOREIGN KEY(interested_property_id) REFERENCES properties(id)
            )
        ''')

        # Tasks table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                due_date TIMESTAMP,
                assigned_to INTEGER,
                priority TEXT,
                status TEXT,
                created_at TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY(assigned_to) REFERENCES contacts(id)
            )
        ''')

        # Documents table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                title TEXT,
                file_path TEXT,
                property_id INTEGER,
                transaction_id INTEGER,
                uploaded_at TIMESTAMP,
                FOREIGN KEY(property_id) REFERENCES properties(id),
                FOREIGN KEY(transaction_id) REFERENCES transactions(id)
            )
        ''')

        # Followups table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS followups (
                id INTEGER PRIMARY KEY,
                lead_id INTEGER,
                scheduled_date TIMESTAMP,
                followup_type TEXT,
                status TEXT,
                notes TEXT,
                FOREIGN KEY(lead_id) REFERENCES leads(id)
            )
        ''')

        # Properties table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                price REAL,
                type TEXT,
                status TEXT DEFAULT 'Available',
                listed_date TIMESTAMP,
                features TEXT,
                location TEXT
            )
        ''')

        # Add indexes for better performance
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_properties_status 
            ON properties(status)
        ''')
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_leads_status 
            ON leads(status)
        ''')
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_tasks_due_date 
            ON tasks(due_date)
        ''')

        self.conn.commit() 

    def create_backup(self, backup_filename):
        try:
            import shutil
            shutil.copy2('data/crm.db', f'data/backups/{backup_filename}')
        except Exception as e:
            logging.error(f"Backup failed: {str(e)}") 