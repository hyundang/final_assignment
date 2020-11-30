import socketserver
import threading
import socket
from _thread import *
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, 
    QLabel, QTextBrowser)
from PyQt5.QtCore import QObject, QThread, QMutex
import time

# HOST = '127.0.0.1'
# PORT = 9999
lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성
# mutex = QMutex()

PASSWORD = 0
isFalse = True
isSame = False
TimeOverUsers = []

class UserManager: 
            # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스
            # ① 채팅 서버로 입장한 사용자의 등록
            # ② 채팅을 종료하는 사용자의 퇴장 관리
            # ③ 사용자가 입장하고 퇴장하는 관리
            # ④ 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송

   def __init__(self):
        self.users = {} # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}

   def addUser(self, username, password, conn, addr): # 사용자 ID를 self.users에 추가하는 함수
        global isFalse
        global TimeOverUsers 
        global isSame       
        if isFalse:
            if password != PASSWORD:
                conn.send('비밀번호가 잘못되었습니다.\n'.encode())
                return None
        isFalse = False
        
        if username in self.users: # 이미 등록된 사용자라면
            if str(username) in TimeOverUsers: # 강제로 튕긴 사용자라면
                # print('재접속')
                if username in TimeOverUsers:
                    TimeOverUsers.remove(username)
                lock.acquire() # 스레드 동기화를 막기위한 락
                self.users[username] = (conn, addr) #(소켓, 주소)
                lock.release() # 업데이트 후 락 해제
                self.sendMessageToAll('[%s]님이 재접속 되었습니다.\n' %username)
                print('+++ 대화 참여자 수 [%d]' %len(self.users))
                return username
            else:
                isSame = True
                conn.send('이미 등록된 사용자입니다.\n'.encode())
                return None
        
        if username == 'quit':
            if username in TimeOverUsers:
                TimeOverUsers.remove(username)
            return None

        # 새로운 사용자를 등록함
        lock.acquire() # 스레드 동기화를 막기위한 락
        self.users[username] = (conn, addr) #(소켓, 주소)
        lock.release() # 업데이트 후 락 해제

        # self.users.append

        self.sendMessageToAll('[%s]님이 입장했습니다.' %username)
        print('+++ 대화 참여자 수 [%d]' %len(self.users))
            
        return username

   def removeUser(self, username): #사용자를 제거하는 함수
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('[%s]님이 퇴장했습니다.' %username)
        print('--- 대화 참여자 수 [%d]' %len(self.users))

   def messageHandler(self, username, msg): # 전송한 msg를 처리하는 부분
        global TimeOverUsers

        if msg.strip() == 'quit': # 보낸 메세지가 'quit'이면
            self.removeUser(username)
            return -1
            
        if msg.strip() == 'timeover':
            # self.removeUser(username)
            # 전역 배열을 만들어서 여기에 username 저장하고,
            # registeruser 부분에서 이 배열에 만약에 저장되어 있는 애면
            # addr만 바꿔줌
            if username not in TimeOverUsers:
                TimeOverUsers.append(username)
            # print(TimeOverUsers)
            print('--- 대화 참여자 수 [%d]' %len(self.users))
            return -2

        if msg[0] != '/': # 보낸 메세지의 첫문자가 '/'가 아니면
            self.sendMessageToAll('[%s] %s' %(username, msg))
            return

    

   def sendMessageToAll(self, msg):
      for conn, addr in self.users.values():
         conn.send(msg.encode())
          

class MyTcpHandler(socketserver.BaseRequestHandler):
   userman = UserManager()
    
   def handle(self): # 클라이언트가 접속시 클라이언트 주소 출력
        print('[%s] 연결됨' %self.client_address[1])
        global isFalse
        isFalse = True
        global isSame
        isSame = False
        try:
            username = self.registerUsername()
            # print(username)
            if username == 'quit':
                self.request.send('채팅이 종료되었습니다.\n'.encode())
                self.request.close()
            elif username == 'false':
                self.request.close()
            else:
                msg = self.request.recv(1024)
                while msg:
                    # print(msg.decode())
                    x = self.userman.messageHandler(username, msg.decode())
                    if x == -1 or x == -2:
                        if x == -1:
                            self.request.send('채팅이 종료되었습니다.\n'.encode())
                            self.request.close()
                        else:
                            self.request.send('시간이 초과되었습니다'.encode())
                            self.userman.sendMessageToAll('[%s]님의 연결이 끊어졌습니다.\n' %username)
                            self.request.close()        
                        break
                    msg = self.request.recv(1024)
                    
        except Exception as e:
            print(e)
            self.userman.removeUser(username)

        print('[%s] 접속종료' %self.client_address[1])
        # self.userman.removeUser(username)

   def registerUsername(self):
        while True:
            global isFalse
            # self.request.send('로그인ID:'.encode())
            username = self.request.recv(1024)
            # password = self.request.recv(1024)
            username = username.decode().strip()
            # password = password.decode().strip()
            arr = username.split(' ')
            username = arr[0]
            password = arr[1]
            if self.userman.addUser(username, int(password), self.request, self.client_address):
                return username
            if isFalse:
                return 'false'
            if isSame:
                return 'false'

class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
        


if __name__ == '__main__':
#    runServer(ex)
#    app = QApplication(sys.argv)
#    ex = Server(app)
#    ex = Window()
#    sys.exit(app.exec_())
    HOST = input("IP 주소를 입력하세요: ")
    PORT = input("port 번호를 입력하세요: ")
    PASS = input("password를 입력하세요: ")
    PASSWORD = int(PASS)
    print("run server")
    try:
        server= ChatingServer((HOST, int(PORT)), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("stop server")
        server.shutdown()
        server.server_close()

        
