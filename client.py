import socket
from threading import Thread
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, 
    QLabel, QTextBrowser, QVBoxLayout, QDialog, QMainWindow)



# class Client(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         btnLogin = QPushButton(self)
#         btnLogin.setText('Login')
#         btnLogin.pressed.connect(self.onLoginClick)
#         btnCancle = QPushButton(self)
#         btnCancle.setText('Cancle')
#         btnCancle.pressed.connect(self.close)

#         btnLogin.move(200, 150)
#         btnCancle.move(450, 150)

#         self.lb1 = QLabel(self)
#         self.lb1.move(30, 20)
#         self.lb1.setText('server IP')
#         self.lb2 = QLabel(self)
#         self.lb2.move(350, 20)
#         self.lb2.setText('password')
#         self.lb3 = QLabel(self)
#         self.lb3.move(30, 70)
#         self.lb3.setText('Port')
#         self.lb4 = QLabel(self)
#         self.lb4.move(350, 70)
#         self.lb4.setText('Name')

#         self.inputIP = QLineEdit(self)
#         self.inputIP.move(100, 20)
#         self.inputIP.returnPressed.connect(self.getIP)
#         self.inputPass = QLineEdit(self)
#         self.inputPass.move(420, 20)
#         self.inputPass.returnPressed.connect(self.getPass)
#         self.inputPort = QLineEdit(self)
#         self.inputPort.move(100, 70)
#         self.inputPort.returnPressed.connect(self.getPort)
#         self.inputName = QLineEdit(self)
#         self.inputName.move(420, 70)
#         self.inputName.returnPressed.connect(self.getName)

#         self.setWindowTitle('Computer Network Chat')
#         self.move(400, 100)
#         self.resize(700, 200)
#         # self.show()

#     # def onLoginClick(self):
#     #     chat = ChatRoom(self)
#     #     chat.exec_()


#     def getIP(self):
#         text = self.inputIP.text()

#     def getPass(self):
#         text = self.inputPass.text()

#     def getPort(self):
#         text = self.inputPort.text()
    
#     def getName(self):
#         text = self.inputName.text()



class ChatRoom(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btnLogin = QPushButton(self)
        self.btnLogin.setText('Login')
        self.btnLogin.pressed.connect(self.onLoginClick)

        self.lb1 = QLabel(self)
        self.lb1.setText('server IP')
        self.lb3 = QLabel(self)
        self.lb3.setText('Port')

        self.inputIP = QLineEdit(self)
        # self.inputIP.returnPressed.connect(self.getIP)
        self.inputPort = QLineEdit(self)
        # self.inputPort.returnPressed.connect(self.getPort)
        
        self.le = QLineEdit(self)
        self.le.returnPressed.connect(self.getText)

        self.tb = QTextBrowser(self)
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)

        self.btnSend = QPushButton('Send')
        # self.btnSend.pressed.connect(self.getText)
        self.btnFile = QPushButton('File')
        # self.btnFile.pressed.connect()
        self.btnQuit = QPushButton('Quit')
        self.btnQuit.pressed.connect(self.onQuit)
        

        vbox = QVBoxLayout()
        vbox.addWidget(self.lb1)
        vbox.addWidget(self.inputIP)
        vbox.addWidget(self.lb3)
        vbox.addWidget(self.inputPort)
        vbox.addWidget(self.btnLogin)
        vbox.addWidget(self.tb)
        vbox.addWidget(self.le)
        vbox.addWidget(self.btnSend)
        vbox.addWidget(self.btnFile)
        vbox.addWidget(self.btnQuit)

        self.setLayout(vbox)

        self.setWindowTitle('Chat Room')
        self.move(400, 100)
        self.resize(800, 800)
        self.show()

    def onLoginClick(self):
        self.host = self.inputIP.text()
        self.port = self.inputPort.text()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, int(self.port)))
        runChat(self, self.sock)
        

    def onQuit(self):
        self.sock.send('/quit'.encode())
        self.tb.append('채팅이 종료되었습니다.')

    def getText(self):
        self.message = self.le.text()
        self.sock.send(self.message.encode())
        self.le.clear()



def rcvMsg(sock, ex):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print('Received from the server :',repr(data.decode()))
            ex.tb.append(data.decode())
        except:
            print('fail')
            pass

def runChat(ex, sock):
    t = Thread(target=rcvMsg, args=(sock,ex))
    t.daemon = True
    t.start()

            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatRoom()
    # runChat(ex)
    sys.exit(app.exec_())
   

