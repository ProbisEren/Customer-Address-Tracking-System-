from PyQt5 import QtWidgets, QtCore
from updateContract_frame import Ui_MainWindow
from CustomerManager import CustomerManager
from AddressManager import AddressManager
from ContractManager import ContractManager
from Contract import Contract
from Address import Address
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery


class UpdateContractWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("main_database.db")
        if not self.db.open():
            print("Veritabanı açılamadı!")

        self.customer_manager = CustomerManager()
        self.address_manager = AddressManager()
        self.contract_manager = ContractManager()

        self.setup_models()

        self.ui.pushButton.clicked.connect(self.get_selected_customer)
        self.ui.pushButton_2.clicked.connect(self.update_contract)

        self.ui.checkBox.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)

        self.ui.signdate_txt.textChanged.connect(self.check_form_complete)
        self.ui.finishdate_txt.textChanged.connect(self.check_form_complete)
        self.ui.rent_txt.textChanged.connect(self.check_form_complete)
        self.ui.fee_txt.textChanged.connect(self.check_form_complete)

        self.ui.checkBox.stateChanged.connect(self.toggle_update_button)

        self.selected_customer_id = None
        self.selected_address_id = None
        self.current_contract_id = None
        self.ui.lineEdit.textChanged.connect(self.filter_customers)

    def setup_models(self):
        self.customer_model = QSqlTableModel(self, self.db)
        self.customer_model.setTable("customers")
        self.customer_model.select()
        self.ui.tableView.setModel(self.customer_model)
        self.ui.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.ui.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)

    def filter_customers(self, text):
        text = text.lower()
        for row in range(self.customer_model.rowCount()):
            name = self.customer_model.data(
                self.customer_model.index(row, self.customer_model.fieldIndex("name"))).lower()
            surname = self.customer_model.data(
                self.customer_model.index(row, self.customer_model.fieldIndex("surname"))).lower()

            # İsim veya soyisim içinde arama metni geçiyorsa göster, geçmiyorsa gizle
            match = (text in name) or (text in surname)
            self.ui.tableView.setRowHidden(row, not match)

    def get_selected_customer(self):
        selected_indexes = self.ui.tableView.selectionModel().selectedRows()
        if not selected_indexes:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen bir müşteri seçin!")
            return

        row = selected_indexes[0].row()
        model = self.customer_model

        # Müşteri bilgilerini direkt modelden çekiyoruz
        name = model.data(model.index(row, model.fieldIndex("name")))
        surname = model.data(model.index(row, model.fieldIndex("surname")))
        age = model.data(model.index(row, model.fieldIndex("age")))
        email = model.data(model.index(row, model.fieldIndex("email")))
        phone = model.data(model.index(row, model.fieldIndex("phone_number")))
        customer_id = model.data(model.index(row, model.fieldIndex("id")))
        address_id = model.data(model.index(row, model.fieldIndex("address_id")))

        self.selected_customer_id = customer_id
        self.selected_address_id = address_id

        # Müşteri bilgilerini label'lara yaz
        self.ui.name_surname_lbl.setText(f"{name} {surname}")
        self.ui.age_lbl.setText(str(age))
        self.ui.mail_lbl.setText(email)
        self.ui.phone_no_lbl.setText(phone)

        # Adres bilgilerini de modelden alıp label'lara yazalım
        if address_id:
            # Adres bilgilerini tableView modelinden bulacağız
            found_address = False
            # Burada adres modeli yoksa, eğer varsa kullanabilirsin:
            # for row_idx in range(self.address_model.rowCount()):
            #     id_ = self.address_model.data(self.address_model.index(row_idx, self.address_model.fieldIndex("id")))
            #     if id_ == address_id:
            #         city = self.address_model.data(self.address_model.index(row_idx, self.address_model.fieldIndex("city")))
            #         ...
            #         found_address = True
            #         break

            # Eğer address_model yoksa veritabanından çekmek istersen aşağıdaki gibi
            query = QSqlQuery(self.db)
            query.prepare("""
                          SELECT city, district, neighborhood, street, building_no, flat_no, postal_code
                          FROM addresses
                          WHERE id = ?
                          """)
            query.addBindValue(address_id)
            if query.exec() and query.next():
                city = query.value(0)
                district = query.value(1)
                neighborhood = query.value(2)
                street = query.value(3)
                building_no = query.value(4)
                flat_no = query.value(5)
                postal_code = query.value(6)
                found_address = True

                self.ui.city_lbl.setText(city)
                self.ui.district_lbl.setText(district)
                self.ui.nb_lbl.setText(neighborhood)
                self.ui.street_lbl.setText(street)
                self.ui.bno_lbl.setText(str(building_no))
                self.ui.flat_no_lbl.setText(str(flat_no))
                self.ui.postal_code_lbl.setText(str(postal_code))

            if not found_address:
                self.clear_address_labels()
        else:
            self.clear_address_labels()

    def clear_address_labels(self):
        self.ui.city_lbl.setText("")
        self.ui.district_lbl.setText("")
        self.ui.nb_lbl.setText("")
        self.ui.street_lbl.setText("")
        self.ui.bno_lbl.setText("")
        self.ui.flat_no_lbl.setText("")
        self.ui.postal_code_lbl.setText("")

    def get_address_by_id(self, address_id):
        if not address_id:
            return None
        query = QSqlQuery(self.db)
        query.prepare("SELECT city, district, neighborhood, street, building_no, flat_no, postal_code FROM addresses WHERE id = ?")
        query.addBindValue(address_id)
        if query.exec() and query.next():
            city = query.value(0)
            district = query.value(1)
            neighborhood = query.value(2)
            street = query.value(3)
            building_no = query.value(4)
            flat_no = query.value(5)
            postal_code = query.value(6)
            return Address(city, district, neighborhood, street, building_no, flat_no, postal_code)
        return None

    def check_form_complete(self):
        fields = [
            self.ui.signdate_txt.text().strip(),
            self.ui.finishdate_txt.text().strip(),
            self.ui.rent_txt.text().strip(),
            self.ui.fee_txt.text().strip()
        ]
        all_filled = all(fields)

        self.ui.checkBox.setEnabled(all_filled)
        if not self.ui.checkBox.isEnabled():
            self.ui.checkBox.setChecked(False)

        if not self.ui.checkBox.isChecked():
            self.ui.pushButton_2.setEnabled(False)

    def toggle_update_button(self):
        self.ui.pushButton_2.setEnabled(self.ui.checkBox.isChecked())

    def update_contract(self):
        if not self.selected_customer_id or not self.selected_address_id:
            QtWidgets.QMessageBox.warning(self, "Hata", "Müşteri veya adres seçimi eksik!")
            return

        signing_date = self.ui.signdate_txt.text().strip()
        finish_date = self.ui.finishdate_txt.text().strip()
        try:
            rent = float(self.ui.rent_txt.text().strip())
            cancellation_fee = float(self.ui.fee_txt.text().strip())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Hata", "Kira ve fesih bedeli sayısal olmalı!")
            return

        # 1. Eski kontratı güncelle (finish_date = "Kontrat güncellendi")
        old_contract = self.contract_manager.get_contract_by_customer_address(self.selected_customer_id,
                                                                              self.selected_address_id)

        if old_contract:
            old_contract_id = old_contract["contract_id"]
            self.contract_manager.update_contract(
                old_contract_id,
                old_contract["rent"],
                old_contract["signing_date"],
                "Kontrat güncellendi",
                old_contract["cancellation_fee"]
            )
            print(f"Contract {old_contract_id} güncellendi.")

        # 2. Yeni kontrat oluştur
        new_contract = Contract(
            customer_id=self.selected_customer_id,
            address_id=self.selected_address_id,
            kira=rent,
            imza_tarihi=signing_date,
            finish_date=finish_date,
            fesih_bedeli=cancellation_fee,
            notlar=None
        )

        # 3. Yeni kontratı veritabanına ekle ve yeni kontrat ID'sini al
        try:
            new_contract_id = self.contract_manager.add_contract(new_contract)
            print(f"Yeni kontrat eklendi: ID {new_contract_id}")
        except Exception as e:
            print(f"Yeni kontrat eklenirken hata: {e}")
            QtWidgets.QMessageBox.critical(self, "Hata", "Yeni kontrat eklenirken hata oluştu!")
            return

        # 4. Müşteri tablosundaki contract_id'yi yeni kontrat ID'siyle güncelle
        try:
            conn = self.contract_manager.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE customers SET contract_id = ? WHERE id = ?',
                           (new_contract_id, self.selected_customer_id))
            conn.commit()
            conn.close()
            print(f"Müşteri {self.selected_customer_id} için contract_id {new_contract_id} olarak güncellendi.")
        except Exception as e:
            print(f"Müşteri contract_id güncellenirken hata: {e}")
            QtWidgets.QMessageBox.critical(self, "Hata", "Müşteri contract_id güncellenirken hata oluştu!")
            return

        QtWidgets.QMessageBox.information(self, "Başarılı",
                                          "Sözleşme başarıyla güncellendi ve yeni kontrat oluşturuldu.")
        self.ui.checkBox.setChecked(False)
        self.ui.pushButton_2.setEnabled(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = UpdateContractWindow()
    window.show()
    sys.exit(app.exec_())
