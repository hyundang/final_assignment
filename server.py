# from socket import *
# from select import *

# HOST = ''
# PORT = 10000
# BUFSIZE = 1024
# ADDR = (HOST, PORT)

# # 소켓 생성
# serverSocket = socket(AF_INET, SOCK_STREAM)

# # 소켓 주소 정보 할당 
# serverSocket.bind(ADDR)
# print('bind')

# # 연결 수신 대기 상태
# serverSocket.listen(100)
# print('listen')

# # 연결 수락
# clientSocekt, addr_info = serverSocket.accept()
# print('accept')
# print('--client information--')
# print(clientSocekt)

# # 클라이언트로부터 메시지를 가져옴
# data = clientSocekt.recv(65535)
# print('recieve data : ',data.decode())

# # 소켓 종료 
# clientSocekt.close()
# serverSocket.close()
# print('close')

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel


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


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = Client()
   sys.exit(app.exec_())
