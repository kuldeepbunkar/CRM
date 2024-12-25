from datetime import datetime, timedelta
from models.contact import Contact
from models.property import Property
from models.transaction import Transaction
from models.lead import Lead
from models.task import Task
from services.email_service import EmailService
from services.analytics import AnalyticsService
from services.report_service import ReportService
from utils.validators import DataValidator
import logging

class CRM:
    def __init__(self):
        self.db = Database()
        self.email_service = EmailService()
        self.analytics = AnalyticsService(self.db)
        self.report_service = ReportService(self)
        self.validator = DataValidator()

    # Contact Management
    def add_contact(self, name, email, phone=None, address=None):
        contact = Contact(name, email, phone, address)
        # Save to database
        self.db.cursor.execute('''
            INSERT INTO contacts (name, email, phone, address, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (contact.name, contact.email, contact.phone, contact.address, contact.created_at))
        self.db.conn.commit()
        return contact
    
    def get_contact(self, contact_id):
        self.db.cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
        return self.db.cursor.fetchone()
    
    def update_contact(self, contact_id, **kwargs):
        updates = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        query = f'UPDATE contacts SET {updates} WHERE id = ?'
        self.db.cursor.execute(query, (*kwargs.values(), contact_id))
        self.db.conn.commit()

    # Property Management
    def add_property(self, name, address, price=None, property_type=None, status="Available"):
        property_obj = Property(name, address, price, property_type, status)
        # Save to database
        self.db.cursor.execute('''
            INSERT INTO properties (name, address, price, type, status, listed_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (property_obj.name, property_obj.address, property_obj.price, 
              property_obj.type, property_obj.status, property_obj.listed_date))
        self.db.conn.commit()
        return property_obj
    
    def get_property(self, property_id):
        """Get property with validation"""
        try:
            if not isinstance(property_id, int) or property_id <= 0:
                logging.error(f"Invalid property ID: {property_id}")
                return None
                
            self.db.cursor.execute('SELECT * FROM properties WHERE id = ?', (property_id,))
            property_data = self.db.cursor.fetchone()
            if not property_data:
                logging.error(f"Property not found with ID: {property_id}")
                return None
                
            return property_data
        except Exception as e:
            logging.error(f"Error getting property: {str(e)}")
            return None
    
    def update_property_status(self, property_id, new_status):
        self.db.cursor.execute('''
            UPDATE properties SET status = ? WHERE id = ?
        ''', (new_status, property_id))
        self.db.conn.commit()

    # Transaction Management
    def create_transaction(self, amount, stage, property_id, client_id):
        transaction = Transaction(amount, stage, property_id, client_id)
        self.db.cursor.execute('''
            INSERT INTO transactions 
            (amount, stage, property_id, client_id, transaction_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (transaction.amount, transaction.stage, transaction.property_id,
              transaction.client_id, transaction.transaction_date, transaction.status))
        self.db.conn.commit()
        return transaction
    
    def update_transaction_stage(self, transaction_id, new_stage):
        self.db.cursor.execute('''
            UPDATE transactions SET stage = ? WHERE id = ?
        ''', (new_stage, transaction_id))
        self.db.conn.commit()

    # Email Communications
    def send_property_notification(self, contact_id, property_id):
        contact = self.get_contact(contact_id)
        property_details = self.get_property(property_id)
        
        subject = f"New Property Listing: {property_details['name']}"
        body = f"""
        Dear {contact['name']},
        
        We have a new property that might interest you:
        
        {property_details['name']}
        Address: {property_details['address']}
        Price: ${property_details['price']}
        
        Please let us know if you would like to schedule a viewing.
        
        Best regards,
        Next Innovation Realty
        """
        
        self.email_service.send_email(contact['email'], subject, body)

    # Reporting
    def get_active_properties(self):
        self.db.cursor.execute('SELECT * FROM properties WHERE status = "Available"')
        return self.db.cursor.fetchall()
    
    def get_transactions_by_stage(self, stage):
        self.db.cursor.execute('SELECT * FROM transactions WHERE stage = ?', (stage,))
        return self.db.cursor.fetchall()
    
    def get_monthly_sales_report(self, year, month):
        self.db.cursor.execute('''
            SELECT SUM(amount) as total_sales, COUNT(*) as transaction_count
            FROM transactions
            WHERE strftime('%Y-%m', transaction_date) = ?
            AND status = "Completed"
        ''', (f"{year}-{month:02d}",))
        return self.db.cursor.fetchone()

    # Lead Management
    def add_lead(self, name, email, source, interest_type=None):
        self.db.cursor.execute('''
            INSERT INTO leads (name, email, source, interest_type, created_at, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, source, interest_type, datetime.now(), "New"))
        self.db.conn.commit()

    def update_lead_status(self, lead_id, new_status):
        self.db.cursor.execute('UPDATE leads SET status = ? WHERE id = ?', 
                             (new_status, lead_id))
        self.db.conn.commit()

    # Task Management
    def create_task(self, title, description, due_date, assigned_to, priority="Medium"):
        self.db.cursor.execute('''
            INSERT INTO tasks (title, description, due_date, assigned_to, 
                             priority, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, due_date, assigned_to, priority, "Pending", datetime.now()))
        self.db.conn.commit()

    def complete_task(self, task_id):
        self.db.cursor.execute('''
            UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?
        ''', ("Completed", datetime.now(), task_id))
        self.db.conn.commit()

    # Document Management
    def add_document(self, title, file_path, property_id=None, transaction_id=None):
        self.db.cursor.execute('''
            INSERT INTO documents (title, file_path, property_id, transaction_id, 
                                 uploaded_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, file_path, property_id, transaction_id, datetime.now()))
        self.db.conn.commit()

    # Advanced Search and Filtering
    def search_properties(self, **filters):
        query = 'SELECT * FROM properties WHERE 1=1'
        params = []
        
        if 'min_price' in filters:
            query += ' AND price >= ?'
            params.append(filters['min_price'])
        if 'max_price' in filters:
            query += ' AND price <= ?'
            params.append(filters['max_price'])
        if 'property_type' in filters:
            query += ' AND type = ?'
            params.append(filters['property_type'])
        if 'status' in filters:
            query += ' AND status = ?'
            params.append(filters['status'])
            
        self.db.cursor.execute(query, params)
        return self.db.cursor.fetchall()

    # Analytics and Reporting
    def get_lead_conversion_rate(self, start_date, end_date):
        self.db.cursor.execute('''
            SELECT 
                COUNT(CASE WHEN status = 'Converted' THEN 1 END) * 100.0 / COUNT(*) 
                as conversion_rate
            FROM leads
            WHERE created_at BETWEEN ? AND ?
        ''', (start_date, end_date))
        return self.db.cursor.fetchone()['conversion_rate']

    def get_property_performance(self, property_id):
        self.db.cursor.execute('''
            SELECT 
                p.name,
                p.price,
                COUNT(DISTINCT v.id) as total_viewings,
                COUNT(DISTINCT l.id) as interested_leads,
                AVG(v.rating) as average_rating
            FROM properties p
            LEFT JOIN viewings v ON p.id = v.property_id
            LEFT JOIN leads l ON p.id = l.interested_property_id
            WHERE p.id = ?
            GROUP BY p.id
        ''', (property_id,))
        return self.db.cursor.fetchone()

    # Automated Follow-ups
    def schedule_followup(self, lead_id, followup_date, followup_type):
        self.db.cursor.execute('''
            INSERT INTO followups (lead_id, scheduled_date, followup_type, status)
            VALUES (?, ?, ?, ?)
        ''', (lead_id, followup_date, followup_type, "Pending"))
        self.db.conn.commit()

    def get_due_followups(self):
        self.db.cursor.execute('''
            SELECT f.*, l.name, l.email 
            FROM followups f
            JOIN leads l ON f.lead_id = l.id
            WHERE f.scheduled_date <= ? AND f.status = 'Pending'
        ''', (datetime.now(),))
        return self.db.cursor.fetchall() 

    # Property Management
    def get_matching_properties(self, lead_preferences):
        """Find properties matching lead preferences"""
        query = """
            SELECT * FROM properties 
            WHERE status = 'Available'
            AND price BETWEEN ? AND ?
            AND type = ?
        """
        params = [
            lead_preferences.get('min_price', 0),
            lead_preferences.get('max_price', float('inf')),
            lead_preferences.get('property_type')
        ]
        return self.db.execute_query(query, params)

    def notify_matching_leads(self, property_id):
        """Notify leads about matching property"""
        try:
            property_data = self.get_property(property_id)
            if not property_data:
                logging.error(f"Property not found with ID: {property_id}")
                return False
                
            matching_leads = self.find_matching_leads(property_data)
            
            for lead in matching_leads:
                try:
                    self.email_service.send_property_notification(
                        lead.email,
                        property_data,
                        'property_notification.html'
                    )
                    self.create_followup_task(lead.id, property_id)
                except Exception as e:
                    logging.error(f"Failed to notify lead {lead.id}: {str(e)}")
                    continue
            return True
        except Exception as e:
            logging.error(f"Error in notify_matching_leads: {str(e)}")
            return False

    # Lead Management
    def create_followup_task(self, lead_id, property_id=None):
        """Create follow-up task for lead"""
        task = Task(
            title=f"Follow up with lead",
            description="Contact lead about property interest",
            due_date=datetime.now() + timedelta(days=2),
            assigned_to=self.get_available_agent(),
            priority="High"
        )
        self.db.save_task(task)
        return task

    # Analytics and Reporting
    def generate_performance_report(self, start_date, end_date):
        """Generate comprehensive performance report"""
        return {
            'sales': self.analytics.get_sales_metrics(start_date, end_date),
            'leads': self.analytics.get_lead_metrics(),
            'conversions': self.analytics.get_conversion_rates(),
            'agent_performance': self.analytics.get_agent_performance()
        }

    # Utility Methods
    def get_available_agent(self):
        """Get least busy agent for task assignment"""
        query = """
            SELECT agent_id, COUNT(tasks.id) as task_count
            FROM agents
            LEFT JOIN tasks ON tasks.assigned_to = agents.id
            WHERE tasks.status != 'Completed'
            GROUP BY agent_id
            ORDER BY task_count ASC
            LIMIT 1
        """
        return self.db.execute_query(query)[0]

    def backup_database(self):
        """Create backup of database"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.db.create_backup(f'backup_{timestamp}.db') 

    def find_matching_leads(self, property_data):
        """Find leads that match property criteria"""
        try:
            if not property_data or not isinstance(property_data, dict):
                logging.error("Invalid property data provided")
                return []
                
            required_fields = ['type', 'price', 'location']
            if not all(field in property_data for field in required_fields):
                logging.error("Missing required property fields")
                return []
                
            query = """
                SELECT * FROM leads 
                WHERE status = 'Active'
                AND (
                    interest_type = ? 
                    OR price_range_max >= ?
                    OR preferred_location LIKE ?
                )
            """
            params = (
                property_data['type'],
                property_data['price'],
                f"%{property_data['location']}%"
            )
            results = self.db.execute_query(query, params)
            if results is None:
                return []
            return results
        except Exception as e:
            logging.error(f"Error finding matching leads: {str(e)}")
            return [] 

    def get_recent_leads(self, limit=5):
        """Get most recent leads"""
        try:
            self.db.cursor.execute('''
                SELECT * FROM leads 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            return self.db.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error fetching recent leads: {str(e)}")
            return [] 

    def get_pending_tasks(self):
        """Get all pending tasks"""
        try:
            self.db.cursor.execute('''
                SELECT t.*, c.name as assigned_to_name 
                FROM tasks t
                LEFT JOIN contacts c ON t.assigned_to = c.id
                WHERE t.status = 'Pending'
                ORDER BY t.due_date ASC
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error fetching pending tasks: {str(e)}")
            return [] 