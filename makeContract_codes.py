from PyQt5 import QtWidgets
from makecontract_frame import Ui_MakeContract
from AddressManager import AddressManager
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from AddressManager import AddressManager  # Adresleri çekeceğimiz sınıf
from PyQt5.QtCore import QStringListModel
from Customer import Customer
from CustomerManager import CustomerManager
from ContractManager import ContractManager
from Contract import Contract


class MakeContractWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MakeContract()
        self.ui.setupUi(self)

        self.address_manager = AddressManager()
        self.load_addresses_as_list()

        self.ui.pushButton.clicked.connect(self.choose_address)
        self.ui.button.clicked.connect(self.make_contract)

        self.ui.checkBox.setEnabled(False)
        self.ui.button.setEnabled(False)

        self.ui.name_txt.textChanged.connect(self.check_form_complete)
        self.ui.surname_txt.textChanged.connect(self.check_form_complete)
        self.ui.age_txt.textChanged.connect(self.check_form_complete)
        self.ui.email_txt.textChanged.connect(self.check_form_complete)
        self.ui.signdate_txt.textChanged.connect(self.check_form_complete)
        self.ui.finishdate_txt.textChanged.connect(self.check_form_complete)
        self.ui.rent_txt.textChanged.connect(self.check_form_complete)
        self.ui.fee_txt.textChanged.connect(self.check_form_complete)


        self.ui.checkBox.stateChanged.connect(self.toggle_make_button)

        self.ui.address_txt.textChanged.connect(self.search_addresses)


    def check_form_complete(self):
        fields = [
            self.ui.name_txt.text(),
            self.ui.surname_txt.text(),
            self.ui.age_txt.text(),
            self.ui.email_txt.text(),
            self.ui.signdate_txt.text(),
            self.ui.finishdate_txt.text(),
            self.ui.rent_txt.text(),
            self.ui.fee_txt.text()
        ]
        all_filled = all(field.strip() != "" for field in fields)

        # Label'daki adres seçimi kontrolü
        address_chosen = self.ui.label.text() != "Choosen Address"

        # Checkbox'ı ancak tüm alanlar doluysa ve adres seçilmişse aktif yap
        self.ui.checkBox.setEnabled(all_filled and address_chosen)

        if not self.ui.checkBox.isEnabled(): # enable ise check'i kaldır
            self.ui.checkBox.setChecked(False)

        if not self.ui.checkBox.isChecked():
            self.ui.button.setEnabled(False)


    def toggle_make_button(self):
        # Buton, checkbox işaretli ise aktif olur
        self.ui.button.setEnabled(self.ui.checkBox.isChecked())

    #def choose_address(self):
    #    print("Adres seçme penceresi açılacak")

    def make_contract(self):
        # Müşteri bilgilerini al
        name = self.ui.name_txt.text().strip()
        surname = self.ui.surname_txt.text().strip()
        age = int(self.ui.age_txt.text().strip())
        email = self.ui.email_txt.text().strip()
        phone = self.ui.pno_txt.text().strip()

        # Seçilen adresin ID'sini al (labelda string olduğu için DB'den karşılık bulmamız lazım)
        selected_address_text = self.ui.label.text()

        if selected_address_text == "Choosen Address":
            QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen bir adres seçin!")
            return

        # AddressManager üzerinden ID al
        address_id = self.get_address_id_by_text(selected_address_text)
        if address_id is None:
            QtWidgets.QMessageBox.warning(self, "Hata", "Adres bulunamadı!")
            return

        # Customer nesnesi oluştur (contract_id henüz yok)
        customer = Customer(name, surname, age, phone, email, address_id, None)
        CustomerManager.add_customer(customer)

        # Eklenen müşterinin ID'sini DB'den al (en son eklenen)
        customer_id = self.get_last_customer_id()

        # Kontrat bilgilerini al
        rent = float(self.ui.rent_txt.text())
        signing_date = self.ui.signdate_txt.text().strip()
        finish_date = self.ui.finishdate_txt.text().strip()
        cancellation_fee = float(self.ui.fee_txt.text())
        notlar = None  # Eğer varsa not alanı ekle

        # Contract nesnesi oluştur
        contract = Contract(customer_id, address_id, rent, signing_date, finish_date, cancellation_fee, notlar)

        # Kontratı DB'ye ekle ve müşteri kaydını güncelle
        contract_id = ContractManager.add_contract(contract)


        QtWidgets.QMessageBox.information(self, "Başarılı", f"Kontrat oluşturuldu. ID: {contract_id}")
        # Adresi rented = 1 yap (kiralandı)
        self.address_manager.set_address_rented(address_id, True)

        # Ardından istersen adres listesini güncelle
        self.load_addresses_as_list()

        # Gerekirse formu temizle veya başka işlem yap

    def get_address_id_by_text(self, text):
        # Tüm adresleri al, eşleşeni bul
        addresses = self.address_manager.get_available_addresses()
        for addr in addresses:
            combined = f"{addr[1]}, {addr[2]}, {addr[3]}, {addr[4]}, Bldg No: {addr[5]}, Flat No: {addr[6]}, Postal Code: {addr[7]}"
            if combined == text:
                return addr[0]
        return None

    def get_last_customer_id(self):
        conn = CustomerManager.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(id) FROM customers')
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def load_addresses_as_list(self):
        addresses = self.address_manager.get_available_addresses()
        display_list = []
        for addr in addresses:

            combined = f"{addr[1]}, {addr[2]}, {addr[3]}, {addr[4]}, Bldg No: {addr[5]}, Flat No: {addr[6]}, Postal Code: {addr[7]}"
            display_list.append(combined)

        self.model = QStringListModel()
        self.model.setStringList(display_list)
        self.ui.listView.setModel(self.model)

    def choose_address(self):
        selected_indexes = self.ui.listView.selectedIndexes()
        if selected_indexes:
            index = selected_indexes[0]
            selected_text = self.model.data(index, QtCore.Qt.DisplayRole)
            self.ui.label.setText(selected_text)
            print("Seçilen adres:", selected_text)
        else:
            print("Adres seçilmedi.")
            self.ui.label.setText("Choosen Address")

        # Burada checkbox kontrolünü çağır
        self.check_form_complete()

    def search_addresses(self):
        keyword = self.ui.address_txt.text().strip()
        if keyword == "":
            addresses = self.address_manager.get_available_addresses()
        else:
            addresses = self.address_manager.search_addresses(keyword)

        display_list = []
        for addr in addresses:
            combined = f"{addr[1]}, {addr[2]}, {addr[3]}, {addr[4]}, Bldg No: {addr[5]}, Flat No: {addr[6]}, Postal Code: {addr[7]}"
            display_list.append(combined)

        self.model.setStringList(display_list)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MakeContractWindow()
    window.show()
    sys.exit(app.exec_())
