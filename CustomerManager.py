from DatabaseManager import *
from Customer import Customer

class CustomerManager:
    db_manager = DatabaseManager()

    @classmethod
    def add_customer(cls, customer):
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO customers (name, surname, age, phone_number, email,address_id,contract_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (customer.get_name(), customer.get_surname(), customer.get_age(),
             customer.get_phone_number(), customer.get_email(),customer.get_address_id(),customer.get_contract_id())
        )
        conn.commit()
        conn.close()
        print("Müşteri eklendi.")

    @classmethod
    def delete_customer_by_id(cls, customer_id):
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        conn.commit()
        conn.close()
        print(f"ID'si {customer_id} olan müşteri silindi.")

    @classmethod
    def get_all_customers(cls):
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, surname, age, phone_number, email, address_id, contract_id FROM customers')
        rows = cursor.fetchall()
        conn.close()

        customers = []
        for row in rows:
            customer = Customer(
                name=row[1],
                surname=row[2],
                age=row[3],
                phone_number=row[4],
                email=row[5],
                address_id=row[6],
                contract_id=row[7]
            )
            customers.append(customer)

        return customers

    @classmethod
    def remove_customer_address(cls, customer_id): # süresi geçen veya sözleşmeyi feseheden kiracıların address idlerinin null yapılması ama databasedeb silinmemesi
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE customers SET address_id = NULL WHERE id = ?', (customer_id,))
        conn.commit()
        conn.close()
        print(f"Customer ID {customer_id} adres bağlantısı kaldırıldı.")