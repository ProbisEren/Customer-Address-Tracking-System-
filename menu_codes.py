from PyQt5 import QtWidgets
from menu_frame import Ui_MainWindow       # Menü UI dosyan
from makeContract_codes import MakeContractWindow  # MakeContract kodları içeren pencere sınıfın
from infos_codes import InfosWindow
from addAddress_codes import AddAddressWindow
from updateContract_codes import UpdateContractWindow

class MenuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Make Contract penceresini None olarak başlat
        self.make_contract_window = None


        self.see_infos_window = None
        self.addAddress_window = None
        self.updateContract_window = None

        # Buton click bağlantısı
        self.ui.pushButton.clicked.connect(self.open_make_contract)

        # 2. buton
        self.ui.pushButton_2.clicked.connect(self.open_see_infos)

        self.ui.pushButton_3.clicked.connect(self.open_update_contract_window)

        self.ui.pushButton_4.clicked.connect(self.open_add_address)



    def open_make_contract(self):
        if self.make_contract_window is None:
            self.make_contract_window = MakeContractWindow()
        self.make_contract_window.show()
        self.make_contract_window.raise_()
        self.make_contract_window.activateWindow()

    def open_update_contract_window(self):
        if self.updateContract_window is None:
            self.updateContract_window = UpdateContractWindow()
        self.updateContract_window.show()
        self.updateContract_window.raise_()
        self.updateContract_window.activateWindow()

    def open_see_infos(self):
        if self.see_infos_window is None:
            self.see_infos_window = InfosWindow()
        self.see_infos_window.show()
        self.see_infos_window.raise_()
        self.see_infos_window.activateWindow()

    def open_add_address(self):
        if self.addAddress_window is None:
            self.addAddress_window = AddAddressWindow()
        self.addAddress_window.show()
        self.addAddress_window.raise_()
        self.addAddress_window.activateWindow()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec_())
