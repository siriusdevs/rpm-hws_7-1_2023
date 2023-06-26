import sys
import socket
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QSplitter, QVBoxLayout, QDialog,
    QPushButton, QApplication, QTextEdit, QLineEdit,
)

conn = None


class Window(QDialog):
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
        self.setWindowTitle("Chat Application: Server")
        self.resize(500, 500)

    def send(self):
        text = self.chatTextField.text()
        font = self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        text_formatted = f'U: {text}'
        self.chat.append(text_formatted)
        global conn
        conn.send(text.encode("utf-8"))
        self.chatTextField.setText("")


class ServerThread(Thread):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def run(self):
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpServer.bind(('0.0.0.0', 80))
        tcpServer.listen(4)
        while True:
            print("Multithreaded Python server : Waiting for connections from TCP clients...")
            global conn
            (conn, (ip, port)) = tcpServer.accept()
            newthread = ClientThread(ip, port, self.window)
            newthread.start()


class ClientThread(Thread):

    def __init__(self, ip, port, window):
        super().__init__()
        self.window = window
        self.ip = ip
        self.port = port
        print(f"[+] New server socket thread started for {ip}:{port}")

    def run(self):
        while True:
            global conn
            data = conn.recv(2048)
            self.window.chat.append(f"client: {data.decode('utf-8')}")
            print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        window = Window()
        server_thread = ServerThread(window)
        server_thread.start()
        window.exec()
    except KeyboardInterrupt:
        print('Goodbye!')
    finally:
        sys.exit()
