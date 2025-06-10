import sys
from PyQt5 import QtWidgets
from login_frame import Ui_login_frame  # UI sınıfını içe aktar
from menu_codes import MenuWindow
from DatabaseManager import DatabaseManager

class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        db = DatabaseManager()
        db.create_all_tables()
        self.ui = Ui_login_frame()
        self.ui.setupUi(self)

        # Buton tıklama olayını bağla
        self.ui.pushButton.clicked.connect(self.handle_login)

        self.menu_window = None

    def handle_login(self):
        username = self.ui.username_txt.text()
        password = self.ui.password_txt.text()

        if username == "admin" and password == "admin123":
            print("şifre doğru")
            # menuye geç

            if self.menu_window is None:
                self.menu_window = MenuWindow()
            self.menu_window.show()
            self.menu_window.raise_()
            self.menu_window.activateWindow()
            self.close()#login sayfasını kapıyo

        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Username or Password is incorrect!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
