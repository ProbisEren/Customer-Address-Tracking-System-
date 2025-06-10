from PyQt5 import QtWidgets, QtCore
from infos_frame import Ui_MainWindow  # ui dosyan
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery


class InfosWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Veritabanı bağlantısı
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("main_database.db")
        if not self.db.open():
            print("Database açılamadı!")

        # Modelleri hazırla ve tableView'lere ata
        self.setup_models()

        # Başlangıçta detay label'larını gizle
        self.hide_detail_labels()

        # Butonlara tıklama olaylarını bağla
        self.ui.pushButton.clicked.connect(self.show_customer_details)
        self.ui.pushButton_2.clicked.connect(self.show_address_details)

        self.ui.lineEdit.textChanged.connect(self.filter_customers)
        self.ui.lineEdit_2.textChanged.connect(self.filter_addresses)

    def setup_models(self):
        # Müşteri modeli
        self.customer_model = QSqlTableModel(self, self.db)
        self.customer_model.setTable("customers")
        self.customer_model.select()
        self.ui.tableView.setModel(self.customer_model)
        self.ui.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.ui.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)

        # Adres modeli
        self.address_model = QSqlTableModel(self, self.db)
        self.address_model.setTable("addresses")
        self.address_model.select()
        self.ui.tableView_2.setModel(self.address_model)
        self.ui.tableView_2.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.ui.tableView_2.setSelectionMode(QtWidgets.QTableView.SingleSelection)

    def hide_detail_labels(self):
        labels = [
            self.ui.name_surname_lbl, self.ui.age_lbl, self.ui.mail_lbl, self.ui.phone_no_lbl,
            self.ui.city_lbl, self.ui.district_lbl, self.ui.nb_lbl, self.ui.street_lbl,
            self.ui.bno_lbl, self.ui.flat_no_lbl, self.ui.postal_code_lbl,
            self.ui.rent_lbl, self.ui.sigdate_lbl, self.ui.finishdate_lbl, self.ui.fee_lbl
        ]
        for label in labels:
            label.setVisible(False)

    def show_detail_labels(self):
        labels = [
            self.ui.name_surname_lbl, self.ui.age_lbl, self.ui.mail_lbl, self.ui.phone_no_lbl,
            self.ui.city_lbl, self.ui.district_lbl, self.ui.nb_lbl, self.ui.street_lbl,
            self.ui.bno_lbl, self.ui.flat_no_lbl, self.ui.postal_code_lbl,
            self.ui.rent_lbl, self.ui.sigdate_lbl, self.ui.finishdate_lbl, self.ui.fee_lbl
        ]
        for label in labels:
            label.setVisible(True)

    def clear_contract_labels(self):
        self.ui.rent_lbl.setText("")
        self.ui.sigdate_lbl.setText("")
        self.ui.finishdate_lbl.setText("")
        self.ui.fee_lbl.setText("")

    def show_only_address_empty(self):
        self.ui.name_surname_lbl.setVisible(True)
        self.ui.name_surname_lbl.setText("Adres boş")

        for label in [
            self.ui.age_lbl, self.ui.mail_lbl, self.ui.phone_no_lbl,
            self.ui.city_lbl, self.ui.district_lbl, self.ui.nb_lbl, self.ui.street_lbl,
            self.ui.bno_lbl, self.ui.flat_no_lbl, self.ui.postal_code_lbl,
            self.ui.rent_lbl, self.ui.sigdate_lbl, self.ui.finishdate_lbl, self.ui.fee_lbl
        ]:
            label.setVisible(False)

    def show_customer_details(self):
        selected_indexes = self.ui.tableView.selectionModel().selectedRows()
        if not selected_indexes:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen bir müşteri seçin!")
            return

        row = selected_indexes[0].row()

        # Müşteri bilgileri
        name = self.customer_model.data(self.customer_model.index(row, self.customer_model.fieldIndex("name")))
        surname = self.customer_model.data(self.customer_model.index(row, self.customer_model.fieldIndex("surname")))
        age = self.customer_model.data(self.customer_model.index(row, self.customer_model.fieldIndex("age")))
        email = self.customer_model.data(self.customer_model.index(row, self.customer_model.fieldIndex("email")))
        phone = self.customer_model.data(self.customer_model.index(row, self.customer_model.fieldIndex("phone_number")))

        # Müşteri adres id'sini al
        address_id = self.customer_model.data(
            self.customer_model.index(row, self.customer_model.fieldIndex("address_id")))

        # Adres bilgileri için varsayılan boş değerler
        city = district = neighborhood = street = building_no = flat_no = postal_code = ""

        if address_id:
            for addr_row in range(self.address_model.rowCount()):
                aid = self.address_model.data(self.address_model.index(addr_row, self.address_model.fieldIndex("id")))
                if aid == address_id:
                    city = self.address_model.data(
                        self.address_model.index(addr_row, self.address_model.fieldIndex("city")))
                    district = self.address_model.data(
                        self.address_model.index(addr_row, self.address_model.fieldIndex("district")))
                    neighborhood = self.address_model.data(
                        self.address_model.index(addr_row, self.address_model.fieldIndex("neighborhood")))
                    street = self.address_model.data(
                        self.address_model.index(addr_row, self.address_model.fieldIndex("street")))
                    building_no = self.address_model.data(
                        self.address_model.index(addr_row, self.address_model.fieldIndex("building_no")))
                    flat_no = self.address_model.data(
                        self.address_model.index(addr_row, self.address_model.fieldIndex("flat_no")))
                    postal_code = self.address_model.data(
                        self.address_model.index(addr_row, self.address_model.fieldIndex("postal_code")))
                    break

        # Label'lara müşteri ve adres bilgilerini yaz
        self.ui.name_surname_lbl.setText(f"{name} {surname}")
        self.ui.age_lbl.setText(str(age))
        self.ui.mail_lbl.setText(email)
        self.ui.phone_no_lbl.setText(phone)
        self.ui.city_lbl.setText(str(city))
        self.ui.district_lbl.setText(str(district))
        self.ui.nb_lbl.setText(str(neighborhood))
        self.ui.street_lbl.setText(str(street))
        self.ui.bno_lbl.setText(str(building_no))
        self.ui.flat_no_lbl.setText(str(flat_no))
        self.ui.postal_code_lbl.setText(str(postal_code))

        # --- Kontrat bilgileri ---
        customer_id = self.customer_model.data(self.customer_model.index(row, self.customer_model.fieldIndex("id")))

        query = QSqlQuery(self.db)
        query.prepare("""
                      SELECT rent, signing_date, finish_date, cancellation_fee
                      FROM contracts
                      WHERE customer_id = ?
                      ORDER BY id DESC LIMIT 1
                      """)
        query.addBindValue(customer_id)
        if query.exec() and query.next():
            rent = query.value(0)
            signing_date = query.value(1)
            finish_date = query.value(2)
            cancellation_fee = query.value(3)

            self.ui.rent_lbl.setText(f"Rent: {rent}")
            self.ui.sigdate_lbl.setText(f"Signing Date: {signing_date}")
            self.ui.finishdate_lbl.setText(f"Finish Date: {finish_date}")
            self.ui.fee_lbl.setText(f"Cancellation Fee: {cancellation_fee}")
        else:
            self.clear_contract_labels()

        self.show_detail_labels()

    def show_address_details(self):
        selected_indexes = self.ui.tableView_2.selectionModel().selectedRows()
        if not selected_indexes:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen bir adres seçin!")
            return

        row = selected_indexes[0].row()

        # Adres bilgileri
        address_id = self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("id")))
        city = self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("city")))
        district = self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("district")))
        neighborhood = self.address_model.data(
            self.address_model.index(row, self.address_model.fieldIndex("neighborhood")))
        street = self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("street")))
        building_no = self.address_model.data(
            self.address_model.index(row, self.address_model.fieldIndex("building_no")))
        flat_no = self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("flat_no")))
        postal_code = self.address_model.data(
            self.address_model.index(row, self.address_model.fieldIndex("postal_code")))

        # Bu adreste oturan müşteri varsa bul
        customer_found = False
        customer_id = None
        for cust_row in range(self.customer_model.rowCount()):
            cust_address_id = self.customer_model.data(
                self.customer_model.index(cust_row, self.customer_model.fieldIndex("address_id")))
            if cust_address_id == address_id:
                name = self.customer_model.data(
                    self.customer_model.index(cust_row, self.customer_model.fieldIndex("name")))
                surname = self.customer_model.data(
                    self.customer_model.index(cust_row, self.customer_model.fieldIndex("surname")))
                age = self.customer_model.data(
                    self.customer_model.index(cust_row, self.customer_model.fieldIndex("age")))
                email = self.customer_model.data(
                    self.customer_model.index(cust_row, self.customer_model.fieldIndex("email")))
                phone = self.customer_model.data(
                    self.customer_model.index(cust_row, self.customer_model.fieldIndex("phone_number")))
                customer_found = True
                customer_id = self.customer_model.data(
                    self.customer_model.index(cust_row, self.customer_model.fieldIndex("id")))
                break

        # Label'lara adres bilgilerini yaz
        self.ui.city_lbl.setText(str(city))
        self.ui.district_lbl.setText(str(district))
        self.ui.nb_lbl.setText(str(neighborhood))
        self.ui.street_lbl.setText(str(street))
        self.ui.bno_lbl.setText(str(building_no))
        self.ui.flat_no_lbl.setText(str(flat_no))
        self.ui.postal_code_lbl.setText(str(postal_code))

        if customer_found:
            # Müşteri bilgilerini yaz
            self.ui.name_surname_lbl.setText(f"{name} {surname}")
            self.ui.age_lbl.setText(str(age))
            self.ui.mail_lbl.setText(email)
            self.ui.phone_no_lbl.setText(phone)

            # Kontrat bilgilerini çek ve göster
            query = QSqlQuery(self.db)
            query.prepare("""
                          SELECT rent, signing_date, finish_date, cancellation_fee
                          FROM contracts
                          WHERE customer_id = ?
                          ORDER BY id DESC LIMIT 1
                          """)
            query.addBindValue(customer_id)
            if query.exec() and query.next():
                rent = query.value(0)
                signing_date = query.value(1)
                finish_date = query.value(2)
                cancellation_fee = query.value(3)

                self.ui.rent_lbl.setText(f"Rent: {rent}")
                self.ui.sigdate_lbl.setText(f"Signing Date: {signing_date}")
                self.ui.finishdate_lbl.setText(f"Finish Date: {finish_date}")
                self.ui.fee_lbl.setText(f"Cancellation Fee: {cancellation_fee}")

                self.show_detail_labels()
            else:
                self.clear_contract_labels()
                self.show_only_address_empty()
        else:
            # Adreste müşteri yoksa tüm detayları temizle, sadece "Adres boş" göster
            self.ui.name_surname_lbl.setText("Adres boş")
            self.ui.age_lbl.setText("")
            self.ui.mail_lbl.setText("")
            self.ui.phone_no_lbl.setText("")

            self.clear_address_labels()
            self.clear_contract_labels()
            self.show_only_address_empty()

    def clear_address_labels(self):
        self.ui.city_lbl.setText("")
        self.ui.district_lbl.setText("")
        self.ui.nb_lbl.setText("")
        self.ui.street_lbl.setText("")
        self.ui.bno_lbl.setText("")
        self.ui.flat_no_lbl.setText("")
        self.ui.postal_code_lbl.setText("")

    def filter_customers(self, text):
        filter_text = text.lower()
        for row in range(self.customer_model.rowCount()):
            name = self.customer_model.data(self.customer_model.index(row, self.customer_model.fieldIndex("name"))).lower()
            surname = self.customer_model.data(self.customer_model.index(row, self.customer_model.fieldIndex("surname"))).lower()
            email = self.customer_model.data(self.customer_model.index(row, self.customer_model.fieldIndex("email"))).lower()
            phone = self.customer_model.data(self.customer_model.index(row, self.customer_model.fieldIndex("phone_number"))).lower()

            match = (filter_text in name) or (filter_text in surname) or (filter_text in email) or (filter_text in phone)
            self.ui.tableView.setRowHidden(row, not match)

    def filter_addresses(self, text):
        filter_text = text.lower()
        for row in range(self.address_model.rowCount()):
            city = str(self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("city")))).lower()
            district = str(self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("district")))).lower()
            neighborhood = str(self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("neighborhood")))).lower()
            street = str(self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("street")))).lower()
            building_no = str(self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("building_no")))).lower()
            flat_no = str(self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("flat_no")))).lower()
            postal_code = str(self.address_model.data(self.address_model.index(row, self.address_model.fieldIndex("postal_code")))).lower()

            match = (filter_text in city or filter_text in district or filter_text in neighborhood or filter_text in street
                     or filter_text in building_no or filter_text in flat_no or filter_text in postal_code)
            self.ui.tableView_2.setRowHidden(row, not match)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = InfosWindow()
    window.show()
    sys.exit(app.exec_())
