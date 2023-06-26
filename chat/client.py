import socket
from threading import Thread
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QLineEdit, QPushButton, QSplitter, QTextEdit,
    QVBoxLayout, QLabel, QWidget
)

tcpClientA = None


class AuthorizationPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Authorization Page")
        self.setFixedSize(300, 150)
        self.setWindowIcon(QIcon("icon.png"))

        username_label = QLabel("Username: ")
        self.username_field = QLineEdit()

        password_label = QLabel("Password: ")
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(username_label)
        layout.addWidget(self.username_field)
        layout.addWidget(password_label)
        layout.addWidget(self.password_field)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_field.text()
        password = self.password_field.text()

        if username == "admin" and password == "admin":
            self.window = MainWindow()
            self.window.show()
            clientThread = ClientThread(self.window)
            clientThread.start()
            self.hide()
        else:
            print("Invalid credentials.")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = 0
        self.chatTextField = QLineEdit(self)
        self.chatTextField.resize(480, 100)
        self.chatTextField.move(10, 350)
        self.btnSend = QPushButton("Send", self)
        self.btnSend.resize(480, 30)
        self.btnSendFont = self.btnSend.font()
        self.btnSendFont.setPointSize(15)
        self.btnSend.setFont(self.btnSendFont)
        self.btnSend.move(10, 460)
        self.btnSend.setStyleSheet("background-color: #8e7cc3")
        self.btnSend.clicked.connect(self.send)
        self.chatBody = QVBoxLayout(self)
        splitter = QSplitter(QtCore.Qt.Vertical)
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        splitter.addWidget(self.chat)
        splitter.addWidget(self.chatTextField)
        splitter.setSizes([400, 100])
        splitter2 = QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.btnSend)
        splitter2.setSizes([200, 10])
        self.chatBody.addWidget(splitter2)
        self.setWindowTitle("Chat Application: Client")
        self.resize(500, 500)

    def send(self):
        text = self.chatTextField.text()
        font = self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted = 'U: ' + text
        print(textFormatted)
        self.chat.append(textFormatted)
        tcpClientA.send(text.encode())
        self.chatTextField.setText("")


class ClientThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        host = socket.gethostname()
        port = 80
        BUFFER_SIZE = 2000
        global tcpClientA
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.connect((host, port))
        while True:
            data = tcpClientA.recv(BUFFER_SIZE)
            self.window.chat.append("server: " + data.decode("utf-8"))


if __name__ == '__main__':
    app = QApplication([])
    window = AuthorizationPage()
    window.show()
    app.exec_()
