import socket
from threading import Thread
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, 
    QLabel, QTextBrowser, QVBoxLayout, QDialog, QMainWindow)
<<<<<<< HEAD


=======
>>>>>>> 0a021faa603e0ee21a6dac3f8a3747f6109ae701
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
        # self.inputIP.returnPressed.connect(self.getIP)
        self.inputPort = QLineEdit(self)
        # self.inputPort.returnPressed.connect(self.getPort)
        self.inputName = QLineEdit(self)
        self.inputPass = QLineEdit(self)
        
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
<<<<<<< HEAD
   
=======
>>>>>>> 0a021faa603e0ee21a6dac3f8a3747f6109ae701

    def onQuit(self):
        self.sock.send('/quit'.encode())
        self.tb.append('채팅이 종료되었습니다.\n')

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
   

