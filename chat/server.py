import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSplitter, QVBoxLayout, QDialog, QPushButton, QApplication, QTextEdit, QLineEdit
import socket
from threading import Thread

conn = None


class Window(QDialog):
    def __init__(self):
        """
        Creates window for chat
        """
        super().__init__()
        self.flag = 0
        self.chatTextField = QLineEdit(self)
        self.chatTextField.resize(480, 100)
        self.chatTextField.move(10, 350)
        self.btnSend=QPushButton("Send",self)
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
        splitter2=QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.btnSend)
        splitter2.setSizes([200, 10])
        self.chatBody.addWidget(splitter2)
        self.setWindowTitle("Chat Application: Server")
        self.resize(500, 500)

    def send(self):
        text=self.chatTextField.text()
        font=self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted = f'U:{text}'
        self.chat.append(textFormatted)
        global conn
        conn.send(text.encode("utf-8"))
        self.chatTextField.setText("")


class ServerThread(Thread):
    def __init__(self, window):
        super().__init__(self)
        self.window = window

    def run(self):
        tcp_ip = '0.0.0.0'
        tcp_port = 80
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.bind((tcp_ip, tcp_port))
        threads = []
        tcp_server.listen(4) 
        while True:
            print("Multithreaded Python server : Waiting for connections from TCP clients...")
            global conn
            (conn, (ip,port)) = tcp_server.accept()
            newthread = ClientThread(ip,port,window)
            newthread.start()
            threads.append(newthread) 


class ClientThread(Thread): 
 
    def __init__(self,ip,port,window): 
        """
        Creates thread for clients
        """
        Thread.__init__(self) 
        self.window = window
        self.ip = ip 
        self.port = port 
        print("[+] New server socket thread started for " + ip + ":" + str(port)) 
 
    def run(self): 
        while True :
            global conn
            data = conn.recv(2048) 
            window.chat.append("client: " + data.decode("utf-8"))
            print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        window = Window()
        serverThread=ServerThread(window)
        serverThread.start()
        window.exec()
    except KeyboardInterrupt:
        print('Goodbye!')
    finally:
        sys.exit()