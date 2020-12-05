import socket
from threading import Thread
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, 
    QLabel, QTextBrowser, QVBoxLayout, QDialog, QMainWindow)
import time
from os.path import exists, getsize

TimeLimit = 10
isLogin = False

class ChatRoom(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
        # ip주소, port 번호, 이름, password 입력 UI

        self.btnLogin = QPushButton(self)
        self.btnLogin.setText('Login')
        self.btnLogin.pressed.connect(self.onLoginClick)
        # 로그인 버튼 UI


        self.tb = QTextBrowser(self)
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)
        # 채팅창 UI

        self.le = QLineEdit(self)
        self.le.returnPressed.connect(self.getText)
        # 채팅 입력칸 UI

        self.btnQuit = QPushButton('Quit')
        self.btnQuit.pressed.connect(self.onQuit)
        # quit 버튼 UI


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
        # ip, port, name, password 문자열 가져옴

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, int(self.port)))
        # 가져온 ip, port 값으로 socket 연결

        runChat(self, self.sock)

        self.sock.send((self.name+' '+self.password).encode())
        # 서버에 이름과 비밀번호 보냄
        
        self.start = time.time()
        # 시간 측정 시작
        
        global isLogin 
        isLogin = True
        self.inputName.clear()
        self.inputPass.clear()
        # 로그인이 성공했다는 표시하고, 이름과 비밀번호 칸 초기화


    def onQuit(self):
        global isLogin
        if isLogin:
          self.sock.send('quit'.encode())
          isLogin = False
        # 만약 채팅 종료가 이미 된 상태라면 실행 안됨.
        # 누르면 서버로 'quit'을 보내고, 채팅 종료됨.



    def getText(self):
        global TimeLimit
        global isLogin
        
        self.timeTerm = time.time() - self.start
        # 새로 채팅을 보내기까지 걸린 시간 측정

        if float(self.timeTerm) > TimeLimit:
            if isLogin:
                # print('timeover')
                self.sock.send('timeover'.encode())
                self.inputName.setText(self.name)
                self.inputPass.setText(self.password)
                isLogin = False
                # 채팅 텀이 TimeLimit 이상이라면 강제로 종료됨.
                # 로그인도 해제되었다고 표시
                # 이름, 비밀번호 창에 기존 값 넣어줌
        else:
            self.message = self.le.text()
            if self.message[0] == '/' and self.message[1] == 's' and self.message[2] == ' ':
                self.sendFileToServer(self.message)

            if self.message[0] == '/' and self.message[1] == 'r' and self.message[2] == ' ':
                self.getFileFromServer(self.message)

            else:
                 self.sock.send(self.message.encode())
            # self.sock.send(self.message.encode())
            self.start = time.time()
            # 채팅 텀이 TimeLimit 이하라면 정상적으로 채팅 작동.
            # 시간 측정 재시작
        self.le.clear()

    def sendFileToServer(self, msg):
        print('111111111111')
        filename = msg[3:]
        if not exists(filename): # 파일이 해당 디렉터리에 존재하지 않으면
            return # 함수를 빠져 나온다.
        self.sock.send(msg.encode())
        print('22222222')
        time.sleep(0.5)
        filesize = getsize(filename)
        filesize = str(filesize)
        self.sock.send(filesize.encode())
        print('33333333333333')
        time.sleep(0.5)

        with open(filename, 'rb') as f:
            try: 
                data = f.read(int(filesize))
                self.sock.send(data)
            except Exception as e:
                print(e)
        print('44444444444')
        return

    def getFileFromServer(self, filename):
	    self.sock.sendall(filename.encode())



def rcvMsg(sock, ex):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            if(data.decode() == 'filestart'):
                fileinfo = sock.recv(1024).decode()
                fileinfo = fileinfo.split('/')
                filename = fileinfo[0]
                filesize = int(fileinfo[1])
                username = fileinfo[2]
                    
                with open(f'{username}_download_{filename}', 'wb') as f:
                    try:
                        data = sock.recv(filesize)
                        f.write(data)
                        
                    except Exception as e:
                            print(e)





            else: # print('Received from the server :',repr(data.decode()))
                ex.tb.append(data.decode())
            # 서버에서 오는 값을 받아서 채팅창 UI에 출력
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
   

