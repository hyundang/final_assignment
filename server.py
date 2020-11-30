import socketserver
import threading
import socket
from _thread import *
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, 
    QLabel, QTextBrowser)
from PyQt5.QtCore import QObject, QThread, QMutex


# HOST = '127.0.0.1'
# PORT = 9999
lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성
# mutex = QMutex()


class UserManager: 
            # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스
            # ① 채팅 서버로 입장한 사용자의 등록
            # ② 채팅을 종료하는 사용자의 퇴장 관리
            # ③ 사용자가 입장하고 퇴장하는 관리
            # ④ 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송

   def __init__(self):
        self.users = {} # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}

   def addUser(self, username, conn, addr): # 사용자 ID를 self.users에 추가하는 함수
        if username in self.users or username == '/quit': # 이미 등록된 사용자라면
            conn.send('이미 등록된 사용자입니다.\n'.encode())
            #  특정 연결된 사용자(소켓)에게만 보내는 것.
            return None


        # 새로운 사용자를 등록함
        lock.acquire() # 스레드 동기화를 막기위한 락
        # mutex.lock()
        self.users[username] = (conn, addr) #(소켓, 주소)
        lock.release() # 업데이트 후 락 해제
        # mutex.unlock()

        # self.users.append

        self.sendMessageToAll('[%s]님이 입장했습니다.' %username)
        print('+++ 대화 참여자 수 [%d]' %len(self.users))
            
        return username

   def removeUser(self, username): #사용자를 제거하는 함수
        if username not in self.users:
            return

        lock.acquire()
        # mutex.lock()
        del self.users[username]
        lock.release()
        # mutex.unlock()

        self.sendMessageToAll('[%s]님이 퇴장했습니다.' %username)
        print('--- 대화 참여자 수 [%d]' %len(self.users))

   def messageHandler(self, username, msg): # 전송한 msg를 처리하는 부분
      if msg[0] != '/': # 보낸 메세지의 첫문자가 '/'가 아니면
         self.sendMessageToAll('[%s] %s' %(username, msg))
         return

      if msg.strip() == '/quit': # 보낸 메세지가 'quit'이면
         self.removeUser(username)
         return -1

   def sendMessageToAll(self, msg):
      for conn, addr in self.users.values():
         conn.send(msg.encode())
          

class MyTcpHandler(socketserver.BaseRequestHandler):
   userman = UserManager()
   print('MyTCPH')
    
   def handle(self): # 클라이언트가 접속시 클라이언트 주소 출력
        print('[%s] 연결됨' %self.client_address[1])
        # ex.tb.append("[" + self.client_address[0] + "]" + " 연결됨")

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                if self.userman.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)
                    
        except Exception as e:
            print(e)

        print('[%s] 접속종료' %self.client_address[1])
        self.userman.removeUser(username)

   def registerUsername(self):
        while True:
            self.request.send('로그인ID:'.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.addUser(username, self.request, self.client_address):
                return username

class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
        

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.bind((HOST, PORT)) 
# server_socket.listen() 

# class Window(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         self.isStart = True

#     def initUI(self):
#         self.btnStart = QPushButton(self)
#         self.btnStart.setText('Start')
#         self.btnStop = QPushButton(self)
#         self.btnStop.setText('Stop')

#         self.btnStart.move(650, 300)
#         self.btnStart.resize(70, 70)
#         self.btnStart.pressed.connect(self.runServer)
#         self.btnStop.move(650, 400)
#         self.btnStop.resize(70, 70)
#         self.btnStop.pressed.connect(self.stopServer)

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
#         self.lb4.move(30, 150)
#         self.lb4.setText('Client List')


#         self.tb = QTextBrowser(self)
#         self.tb.setAcceptRichText(True)
#         self.tb.setOpenExternalLinks(True)
#         self.tb.move(30, 200)
#         self.tb.resize(500, 500)

#         self.inputIP = QLineEdit(self)
#         self.inputIP.move(100, 20)
#         self.inputIP.returnPressed.connect(self.getIP)
#         self.inputPass = QLineEdit(self)
#         self.inputPass.move(420, 20)
#         self.inputPass.returnPressed.connect(self.getPass)
#         self.inputPort = QLineEdit(self)
#         self.inputPort.move(100, 70)
#         self.inputPort.returnPressed.connect(self.getPort)


#         self.setWindowTitle('Computer Network Chat')
#         self.move(400, 100)
#         self.resize(800, 800)
#         self.show()

#     def getIP(self):
#         text = self.inputIP.text()

#     def getPass(self):
#         text = self.inputPass.text()

#     def getPort(self):
#         text = self.inputPort.text()

#     def runServer(self):
#         print('run server')
#         self.tb.append('+++ 채팅 서버를 시작합니다.')
#         self.isStart = True
#         self.server = ChatingServer((HOST, PORT), MyTcpHandler)
#         self.server.serve_forever()
#         # while True:
#         #     client_socket, addr = server_socket.accept()
#         #     self.server_thread = QThread()
#         #     self.
#         #     start_new_thread(threaded, (client_socket, addr))

#     def stopServer(self):
#         self.tb.append('--- 채팅 서버를 종료합니다.')
#         self.isStart = False
#         self.server.shutdown()
#         self.server.server_close()
        # server_socket.close()

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.bind((HOST, PORT)) 
# server_socket.listen() 

# class Server(QObject):
#     def __init__(self, parent=None):
#         super(self.__class__, self).__init__(parent)

#         self.gui = Window()

#         self._connectSignals()

#         self.gui.show()

#     def _connectSignals(self):
#         self.gui.btnStart.clicked.connect(self.runServer)
#         self.gui.btnStop.clicked.connect(self.stopServer)
        
#     def runServer(self):
#         while True:
#             client_socket, addr = server_socket.accept()
#             self.threaded = Threaded(client_socket, addr, self.gui)
#             self.threaded_thread = QThread()
#             self.threaded.moveToThread(self.threaded_thread)
#             self.threaded_thread.start()

#     def stopServer(self):
#         server_socket.close()

# class Threaded(QObject):
#     userman = UserManager()

#     def __init__(self, client_socket, addr, gui):

#         print('[%s] 연결됨' %addr[0])
#         gui.tb.append("[" + addr[0] + "]" + " 연결됨")

#         try:
#             username = self.registerUsername(client_socket, addr)
#             msg = client_socket.recv(1024)
#             while msg:
#                 print(msg.decode())
#                 if self.userman.messageHandler(username, msg.decode()) == -1:
#                     client_socket.close()
#                     break
#                 msg = client_socket.recv(1024)
                    
#         except Exception as e:
#             print(e)

#         print('[%s] 접속종료' %addr[0])
#         self.userman.removeUser(username)


#     def registerUsername(self, client_socket, addr):
#         while True:
#             client_socket.send('로그인ID:'.encode())
#             username = client_socket.recv(1024)
#             username = username.decode().strip()
#             if self.userman.addUser(username, client_socket, addr[0]):
#                 return username


# app = QApplication(sys.argv)
# ex = Window()





if __name__ == '__main__':
#    runServer(ex)
#    app = QApplication(sys.argv)
#    ex = Server(app)
#    ex = Window()
#    sys.exit(app.exec_())
    HOST = input("IP 주소를 입력하세요: ")
    PORT = input("port 번호를 입력하세요: ")
    print("run server")
    try:
        server= ChatingServer((HOST, int(PORT)), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("stop server")
        server.shutdown()
        server.server_close()

        
