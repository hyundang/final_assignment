# import socket 
# from _thread import *


# # 쓰레드에서 실행되는 코드입니다. 

# # 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다. 
# def threaded(client_socket, addr): 

#     print('Connected by :', addr[0], ':', addr[1]) 



#     # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
#     while True: 

#         try:

#             # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
#             data = client_socket.recv(1024)

#             if not data: 
#                 print('Disconnected by ' + addr[0],':',addr[1])
#                 break

#             print('Received from ' + addr[0],':',addr[1] , data.decode())

#             client_socket.send(data) 

#         except ConnectionResetError as e:

#             print('Disconnected by ' + addr[0],':',addr[1])
#             break
             
#     client_socket.close() 


# HOST = '127.0.0.1'
# PORT = 9999

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.bind((HOST, PORT)) 
# server_socket.listen() 

# print('server start')


# # 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.

# # 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
# while True: 

#     print('wait')


#     client_socket, addr = server_socket.accept() 
#     start_new_thread(threaded, (client_socket, addr)) 

# server_socket.close()


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
