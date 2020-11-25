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
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, 
    QLabel, QTextBrowser)


class Server(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btnStart = QPushButton(self)
        self.btnStart.setText('Start')
        self.btnStop = QPushButton(self)
        self.btnStop.setText('Stop')

        self.btnStart.move(650, 300)
        self.btnStart.resize(70, 70)
        self.btnStop.move(650, 400)
        self.btnStop.resize(70, 70)

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
        self.lb4.move(30, 150)
        self.lb4.setText('Client List')


        self.tb = QTextBrowser(self)
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)
        self.tb.move(30, 200)
        self.tb.resize(500, 500)

        self.inputIP = QLineEdit(self)
        self.inputIP.move(100, 20)
        self.inputIP.returnPressed.connect(self.getIP)
        self.inputPass = QLineEdit(self)
        self.inputPass.move(420, 20)
        self.inputPass.returnPressed.connect(self.getPass)
        self.inputPort = QLineEdit(self)
        self.inputPort.move(100, 70)
        self.inputPort.returnPressed.connect(self.getPort)


        self.setWindowTitle('Computer Network Chat')
        self.move(400, 100)
        self.resize(800, 800)
        self.show()

    def getIP(self):
        text = self.inputIP.text()

    def getPass(self):
        text = self.inputPass.text()

    def getPort(self):
        text = self.inputPort.text()



if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = Server()
   sys.exit(app.exec_())
