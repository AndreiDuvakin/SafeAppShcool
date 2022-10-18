import os
import sys
from data.address import Address
from data.user import User

from data import db_session
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5 import uic
from PyQt5.QtCore import QPoint, Qt, QUrl
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
import urllib.request


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("desing/MainWindow.ui", self)
        self.initUI()

    def initUI(self):
        cp = QDesktopWidget().availableGeometry().center()
        self.move(QPoint(int(cp.x() - self.width() / 2), int(cp.y() - self.height() / 2)))
        self.pushButton.clicked.connect(self.go_home)
        self.pushButton_2.clicked.connect(self.go_school)
        self.pushButton_3.clicked.connect(self.show_info)
        self.pushButton_4.clicked.connect(self.setting)
        self.pushButton_5.clicked.connect(self.login)

    def login(self):
        self.login = LoginWindow()
        self.login.show()

    def go_home(self):
        self.go_home = GoHomeWindow()
        self.go_home.show()

    def go_school(self):
        self.go_school = GoSchoolWindow()
        self.go_school.show()

    def show_info(self):
        self.info = InfoWindow()
        self.info.show()

    def setting(self):
        self.setting = SettingWindow()
        self.setting.show()


class GoHomeWindow(QMainWindow):
    def __init__(self):
        super(GoHomeWindow, self).__init__()
        uic.loadUi("desing/GoHomeWindow.ui", self)
        self.initUI()

    def initUI(self):
        self.session = db_session.create_session()
        self.pushButton.clicked.connect(self.back)
        cp = QDesktopWidget().availableGeometry().center()
        self.move(QPoint(int(cp.x() - self.width() / 2), int(cp.y() - self.height() / 2)))
        home_address = self.session.query(Address).filter(Address.type == 'home').first()
        if home_address:
            home_address = home_address.address
        else:
            home_address = None
        school_address = self.session.query(Address).filter(Address.type == 'school').first()
        if school_address:
            school_address = school_address.address
        else:
            school_address = None
        if school_address and home_address:
            with open('static/mapbasics_templates.js', 'r', encoding='utf-8') as file:
                new_file = file.read().split('<point1>')
                new_file = new_file[0] + f'\'{school_address}\'' + new_file[1]
                new_file = new_file.split('<point2>')
                new_file = new_file[0] + f'\'{home_address}\'' + new_file[1]
                with open('static/mapbasics.js', 'w', encoding='utf-8') as new_js:
                    new_js.write(new_file)
            self.web_engine = QWebEngineView(self)
            channel = QWebChannel()
            self.web_engine.page().setWebChannel(channel)
            self.web_engine.setContextMenuPolicy(
                Qt.NoContextMenu)
            url_string = urllib.request.pathname2url(
                os.path.join(os.getcwd(), "templates/map.html"))  # Загрузить локальный файл html
            self.web_engine.load(QUrl(url_string))
            self.gridLayout.addWidget(self.web_engine)

    def back(self):
        self.close()


class GoSchoolWindow(QMainWindow):
    def __init__(self):
        super(GoSchoolWindow, self).__init__()
        uic.loadUi('desing/GoSchoolWindow.ui', self)
        self.initUI()

    def initUI(self):
        self.session = db_session.create_session()
        cp = QDesktopWidget().availableGeometry().center()
        self.move(QPoint(int(cp.x() - self.width() / 2), int(cp.y() - self.height() / 2)))
        self.pushButton.clicked.connect(self.back)
        home_address = self.session.query(Address).filter(Address.type == 'home').first()
        if home_address:
            home_address = home_address.address
        else:
            home_address = None
        school_address = self.session.query(Address).filter(Address.type == 'school').first()
        if school_address:
            school_address = school_address.address
        else:
            school_address = None
        if school_address and home_address:
            with open('static/mapbasics_templates.js', 'r', encoding='utf-8') as file:
                new_file = file.read().split('<point1>')
                new_file = new_file[0] + f'\'{home_address}\'' + new_file[1]
                new_file = new_file.split('<point2>')
                new_file = new_file[0] + f'\'{school_address}\'' + new_file[1]
                with open('static/mapbasics.js', 'w', encoding='utf-8') as new_js:
                    new_js.write(new_file)
            cp = QDesktopWidget().availableGeometry().center()
            self.move(QPoint(int(cp.x() - self.width() / 2), int(cp.y() - self.height() / 2)))
            self.pushButton.clicked.connect(self.back)
            self.web_engine = QWebEngineView(self)
            channel = QWebChannel()
            self.web_engine.page().setWebChannel(channel)
            self.web_engine.setContextMenuPolicy(
                Qt.NoContextMenu)
            url_string = urllib.request.pathname2url(
                os.path.join(os.getcwd(), "templates/map.html"))  # Загрузить локальный файл html
            self.web_engine.load(QUrl(url_string))
            self.gridLayout.addWidget(self.web_engine)

    def back(self):
        self.close()


class SettingWindow(QMainWindow):
    def __init__(self):
        super(SettingWindow, self).__init__()
        uic.loadUi('desing/SettingWindow.ui', self)
        self.initUI()

    def initUI(self):
        self.session = db_session.create_session()
        cp = QDesktopWidget().availableGeometry().center()
        self.move(QPoint(int(cp.x() - self.width() / 2), int(cp.y() - self.height() / 2)))
        self.pushButton.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.save_home)
        self.pushButton_3.clicked.connect(self.save_school)
        address = self.session.query(Address).filter(Address.type == 'school').first()
        if address:
            self.lineEdit_2.setText(address.address)
        address = self.session.query(Address).filter(Address.type == 'home').first()
        if address:
            self.lineEdit.setText(address.address)

    def save_school(self):
        address = self.session.query(Address).filter(Address.type == 'school').first()
        if address:
            address.address = self.lineEdit_2.text()
        else:
            new_address = Address(
                type='school',
                coordinate_x=None,
                coordinate_y=None,
                address=self.lineEdit_2.text()
            )
            self.session.add(new_address)
        self.session.commit()

    def save_home(self):
        address = self.session.query(Address).filter(Address.type == 'home').first()
        if address:
            address.address = self.lineEdit.text()
        else:
            new_address = Address(
                type='home',
                coordinate_x=None,
                coordinate_y=None,
                address=self.lineEdit.text()
            )
            self.session.add(new_address)
        self.session.commit()

    def back(self):
        self.close()


class InfoWindow(QMainWindow):
    def __init__(self):
        super(InfoWindow, self).__init__()
        uic.loadUi('desing/InfoWindow.ui', self)
        self.initUI()

    def initUI(self):
        cp = QDesktopWidget().availableGeometry().center()
        self.move(QPoint(int(cp.x() - self.width() / 2), int(cp.y() - self.height() / 2)))
        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.close()


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi('desing/LoginWindow.ui', self)
        self.initUI()

    def initUI(self):
        cp = QDesktopWidget().availableGeometry().center()
        self.move(QPoint(int(cp.x() - self.width() / 2), int(cp.y() - self.height() / 2)))
        self.pushButton.clicked.connect(self.back)
        self.web_engine = QWebEngineView(self)
        channel = QWebChannel()
        self.web_engine.page().setWebChannel(channel)
        self.web_engine.setContextMenuPolicy(
            Qt.NoContextMenu) # Загрузить локальный файл html
        self.web_engine.load(QUrl('http://127.0.0.1:5000/simple/register'))
        self.gridLayout.addWidget(self.web_engine)

    def back(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    db_session.global_init("db/safe_school.db")
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
