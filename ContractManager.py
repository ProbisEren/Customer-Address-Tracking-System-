from DatabaseManager import DatabaseManager
from Contract import Contract

class ContractManager:
    db_manager = DatabaseManager()

    @classmethod
    def add_contract(cls, contract):
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()

        # Kontrat verilerini ekle
        cursor.execute('''
            INSERT INTO contracts (customer_id, address_id, rent, signing_date, finish_date, cancellation_fee)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            contract.get_customer_id(),
            contract.get_address_id(),
            contract.get_kira(),
            contract.get_imza_tarihi(),
            contract.get_finish_date(),
            contract.get_fesih_bedeli()
        ))
        conn.commit()

        # Yeni eklenen kontrat ID'si
        contract_id = cursor.lastrowid

        # Müşterinin contract_id alanını güncelle
        cursor.execute('UPDATE customers SET contract_id = ? WHERE id = ?', (contract_id, contract.get_customer_id()))
        conn.commit()

        conn.close()
        print(f"Kontrat eklendi ve müşteri contract_id güncellendi: {contract_id}")
        return contract_id

    @classmethod
    def get_contract_by_customer_address(cls, customer_id, address_id):
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, rent, signing_date, finish_date, cancellation_fee
            FROM contracts
            WHERE customer_id = ?
              AND address_id = ?
            ORDER BY id DESC LIMIT 1
        ''', (customer_id, address_id))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "contract_id": row[0],
                "rent": row[1],
                "signing_date": row[2],
                "finish_date": row[3],
                "cancellation_fee": row[4]
            }
        return None

    @classmethod
    def update_contract(cls, contract_id, rent, signing_date, finish_date, cancellation_fee):
        conn = cls.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE contracts
            SET rent             = ?,
                signing_date     = ?,
                finish_date      = ?,
                cancellation_fee = ?
            WHERE id = ?
        ''', (rent, signing_date, finish_date, cancellation_fee, contract_id))
        conn.commit()
        conn.close()
        print(f"Contract {contract_id} güncellendi.")
