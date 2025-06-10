from PyQt5 import QtWidgets
from addaddress_frame import Ui_MainWindow  # Senin UI dosyan
from AddressManager import AddressManager
from Address import Address


class AddAddressWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Başlangıçta buton devre dışı
        self.ui.pushButton.setEnabled(False)

        # Tüm lineEdit'lerin textChanged sinyallerini bağla
        self.ui.city_txt.textChanged.connect(self.check_inputs)
        self.ui.disctrict_txt.textChanged.connect(self.check_inputs)
        self.ui.nb_txt.textChanged.connect(self.check_inputs)
        self.ui.street_txt.textChanged.connect(self.check_inputs)
        self.ui.bno_txt.textChanged.connect(self.check_inputs)
        self.ui.fno_txt.textChanged.connect(self.check_inputs)
        self.ui.pcode_txt.textChanged.connect(self.check_inputs)

        # Buton tıklama olayını bağla
        self.ui.pushButton.clicked.connect(self.add_address)

    def check_inputs(self):
        # Tüm alanların dolu olup olmadığını kontrol et
        edits = [
            self.ui.city_txt,
            self.ui.disctrict_txt,
            self.ui.nb_txt,
            self.ui.street_txt,
            self.ui.bno_txt,
            self.ui.fno_txt,
            self.ui.pcode_txt
        ]
        all_filled = all(edit.text().strip() != "" for edit in edits)
        self.ui.pushButton.setEnabled(all_filled)

    def add_address(self):
        city = self.ui.city_txt.text()
        district = self.ui.disctrict_txt.text()
        neighborhood = self.ui.nb_txt.text()
        street = self.ui.street_txt.text()
        building_no = self.ui.bno_txt.text()
        flat_no = self.ui.fno_txt.text()
        postal_code = self.ui.pcode_txt.text()

        if not (building_no.isdigit() and flat_no.isdigit() and postal_code.isdigit()):
            QtWidgets.QMessageBox.warning(self, "Error", "Building no, Flat no and Postal Code must be numeric!")
            return

        # Address sınıfından bir nesne oluştur (eğer sınıfın varsa)
        print("eren")
        new_address = Address(
            city, district, neighborhood, street,
            int(building_no), int(flat_no), int(postal_code)
        )

        # Veritabanına ekle
        print("eren2")
        AddressManager.add_address(new_address)

        QtWidgets.QMessageBox.information(self, "Success", "Address added successfully!")

        # Formu temizle
        for edit in [self.ui.city_txt, self.ui.disctrict_txt, self.ui.nb_txt, self.ui.street_txt,
                     self.ui.bno_txt, self.ui.fno_txt, self.ui.pcode_txt]:
            edit.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AddAddressWindow()
    window.show()
    sys.exit(app.exec_())
