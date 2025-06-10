from DatabaseManager import DatabaseManager

class AddressManager:

    db_manager = DatabaseManager()

    @classmethod
    def add_address(cls, address):
        print("add_address çağrıldı")
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()
        print("DB bağlantısı açıldı")
        cursor.execute('''
                       INSERT INTO addresses (city, district, neighborhood, street, building_no, flat_no, postal_code,
                                              rented)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (address.get_city(), address.get_district(), address.get_neighborhood(),
                             address.get_street(), address.get_building_no(), address.get_flat_no(),
                             address.get_postal_code(), address.get_rented()))
        print("Insert sorgusu çalıştı")
        conn.commit()
        print("Commit yapıldı")
        conn.close()
        print("Bağlantı kapandı")

    @classmethod
    def get_available_addresses(cls):
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, city, district, neighborhood, street, building_no, flat_no, postal_code
            FROM addresses
            WHERE rented = 0 OR rented IS NULL
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows

    @classmethod
    def search_addresses(cls, keyword):
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()
        query = '''
                SELECT id, \
                       city, \
                       district, \
                       neighborhood, \
                       street, \
                       building_no, \
                       flat_no, \
                       postal_code
                FROM addresses
                WHERE (rented = 0 OR rented IS NULL) \
                  AND (
                    city LIKE ? OR
                    district LIKE ? OR
                    neighborhood LIKE ? OR
                    street LIKE ? OR
                    CAST(building_no AS TEXT) LIKE ? OR
                    CAST(flat_no AS TEXT) LIKE ? OR
                    CAST(postal_code AS TEXT) LIKE ?
                    ) \
                '''
        param = f'%{keyword}%'
        cursor.execute(query, (param, param, param, param, param, param, param))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @classmethod
    def set_address_rented(cls, address_id, rented=True):
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE addresses SET rented = ? WHERE id = ?', (1 if rented else 0, address_id))
        conn.commit()
        conn.close()
        print(f"Address ID {address_id} rented durumu {rented} olarak güncellendi.")


