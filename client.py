import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel,
    QTextBrowser, QVBoxLayout)


class Client(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btnLogin = QPushButton(self)
        btnLogin.setText('Login')
        btnCancle = QPushButton(self)
        btnCancle.setText('Cancle')

        btnLogin.move(200, 150)
        btnCancle.move(450, 150)

        self.lb1 = QLabel(self)
        self.lb1.move(30, 20)
        self.lb1.setText('server IP')
        self.lb2 = QLabel(self)
        self.lb2.move(350, 20)
        self.lb2.setText('password')
        self.lb3 = QLabel(self)
        self.lb3.move(30, 70)
        self.lb3.setText('Port')
        self.lb4 = QLabel(self)
        self.lb4.move(350, 70)
        self.lb4.setText('Name')

        inputIP = QLineEdit(self)
        inputIP.move(100, 20)
        inputPass = QLineEdit(self)
        inputPass.move(420, 20)
        inputPort = QLineEdit(self)
        inputPort.move(100, 70)
        inputName = QLineEdit(self)
        inputName.move(420, 70)

        self.setWindowTitle('Computer Network Chat')
        self.move(400, 100)
        self.resize(700, 200)
        self.show()


class ChatRoom(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chat Room')
        self.move(400, 100)
        self.resize(800, 800)
        self.show()


if __name__ == '__main__':
   #app = QApplication(sys.argv)
   #ex = Client()
   #sys.exit(app.exec_())
   
   app = QApplication(sys.argv)
   ex = ChatRoom()
   sys.exit(app.exec_())


# from socket import *
# from select import *
# import sys
# from time import ctime

# HOST = '127.0.0.1'
# PORT = 10000
# BUFSIZE = 1024
# ADDR = (HOST,PORT)

# clientSocket = socket(AF_INET, SOCK_STREAM)# 서버에 접속하기 위한 소켓을 생성한다.

# try:
# 	clientSocket.connect(ADDR)# 서버에 접속을 시도한다.
# 	clientSocket.send('Hello!'.encode())	# 서버에 메시지 전달

# except  Exception as e:
#     print('%s:%s'%ADDR)
#     sys.exit()

# print('connect is success')