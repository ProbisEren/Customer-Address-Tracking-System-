import sqlite3

class DatabaseManager:
    def __init__(self, db_path="main_database.db"):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        print("Bağlantı kuruldu.")

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def close(self):
        if self.connection:
            self.connection.close()
            print("Bağlantı kapatıldı.")

    def create_customer_table(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                age INTEGER,
                phone_number TEXT,
                email TEXT,
                address_id INTEGER ,
                contract_id INTEGER 
            )
        ''')
        self.connection.commit()
        print("Customer tablosu oluşturuldu.")
        self.close()

    def create_address_table(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS addresses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT,
                        district TEXT,
                        neighborhood TEXT,
                        street TEXT,
                        building_no INTEGER,
                        flat_no INTEGER,
                        postal_code INTEGER,
                        rented BOOLEAN
);
''')
        self.connection.commit()
        print("Address tablosu oluşturuldu.")
        self.close()

    def create_contract_table(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS contracts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id INTEGER NOT NULL,
                        address_id INTEGER NOT NULL,
                        rent REAL,
                        signing_date TEXT,
                        finish_date TEXT,
                        cancellation_fee REAL,
                        FOREIGN KEY (customer_id) REFERENCES customers(id),
                        FOREIGN KEY (address_id) REFERENCES addresses(id)
);
''')
        self.connection.commit()
        print("Contract tablosu oluşturuldu.")
        self.close()

    def create_all_tables(self):
        self.create_customer_table()
        self.create_address_table()
        self.create_contract_table()

