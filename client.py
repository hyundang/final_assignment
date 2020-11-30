import socket
from threading import Thread
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, 
    QLabel, QTextBrowser, QVBoxLayout, QDialog, QMainWindow)
import time



isLogin = False

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
        self.lb4 = QLabel(self)
        self.lb4.setText('Name')
        self.lb5 = QLabel(self)
        self.lb5.setText('Password')

        self.inputIP = QLineEdit(self)
        self.inputPort = QLineEdit(self)
        self.inputName = QLineEdit(self)
        self.inputPass = QLineEdit(self)
        
        self.le = QLineEdit(self)
        self.le.returnPressed.connect(self.getText)

        self.tb = QTextBrowser(self)
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)

        self.btnSend = QPushButton('Send')
        self.btnFile = QPushButton('File')
        self.btnQuit = QPushButton('Quit')
        self.btnQuit.pressed.connect(self.onQuit)
        

        vbox = QVBoxLayout()
        vbox.addWidget(self.lb1)
        vbox.addWidget(self.inputIP)
        vbox.addWidget(self.lb3)
        vbox.addWidget(self.inputPort)
        vbox.addWidget(self.lb4)
        vbox.addWidget(self.inputName)
        vbox.addWidget(self.lb5)
        vbox.addWidget(self.inputPass)
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
        self.name = self.inputName.text()
        self.password = self.inputPass.text()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, int(self.port)))
        runChat(self, self.sock)
        self.sock.send((self.name+' '+self.password).encode())
        self.start = time.time()
        global isLogin 
        isLogin = True
        self.inputName.clear()
        self.inputPass.clear()
        # print(self.start)


    def onQuit(self):
        global isLogin
        if isLogin:
          self.sock.send('quit'.encode())
          isLogin = False
        #   self.inputPort.clear()
        #   self.inputIP.clear()

    def getText(self):
        self.timeTerm = time.time() - self.start

        if float(self.timeTerm) > 10:
            print('timeover')
            self.sock.send('timeover'.encode())
            self.inputName.setText(self.name)
            self.inputPass.setText(self.password)
            global isLogin
            isLogin = False
        else:
            self.message = self.le.text()
            self.sock.send(self.message.encode())
            self.start = time.time()
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
    sys.exit(app.exec_())
   

