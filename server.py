import socketserver
import threading
import socket
from _thread import *
import sys
import time
from os.path import exists, getsize


lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성

PASSWORD = 0
isFalse = True
isSame = False
TimeOverUsers = []


class userHandle: 
   def __init__(self):
        self.users = {} 
        # 사용자 정보가 담길 dictionary
        # {username: (socket, address),...} 형태

   def addUser(self, username, password, conn, addr): # username, socket, address를 users에 추가하는 함수
        global isFalse
        global TimeOverUsers 
        global isSame       
        if isFalse: # 입력된 비밀번호가 잘못되었을 때
            if password != PASSWORD: 
                conn.send('비밀번호가 잘못되었습니다.\n'.encode())
                return None
        
        isFalse = False # 입력된 비밀번호가 올바를 때
        
        if username in self.users: # 이미 등록된 user라면
            if str(username) in TimeOverUsers: # 강제로 종료된 user라면
                # print('재접속')
                if username in TimeOverUsers:  # 강제로 종료된 user 목록에서 username 삭제
                    lock.acquire()
                    TimeOverUsers.remove(username)
                    lock.release()
                lock.acquire() # 스레드 동기화를 막기위한 lock
                self.users[username] = (conn, addr) #users에 추가
                lock.release() # 업데이트 후 lock 해제
                
                self.SendMsgAll('[%s]님이 재접속 되었습니다.\n' %username)
                print('사용자 입장: 대화 참여자 수 [%d]' %len(self.users))
                return username
            else: # 이미 등록된 user
                isSame = True
                conn.send('이미 등록된 사용자입니다.\n'.encode())
                return None
        
        if username == 'quit': # 유저가 quit 버튼 눌렀을 때
            if username in TimeOverUsers:
                lock.acquire()
                TimeOverUsers.remove(username)
                lock.release()
            return None


        # 만약 새로운 사용자라면
        # 새로운 사용자를 등록함
        # lock으로 동기화 방지
        lock.acquire() 
        self.users[username] = (conn, addr)
        lock.release() 


        self.SendMsgAll('[%s]님이 입장했습니다.' %username)
        print('사용자 입장: 대화 참여자 수 [%d]' %len(self.users))
            
        return username



   def deleteUser(self, username): #users에서 사용자 삭제
        if username not in self.users:
            return

        # users에서 사용자 삭제
        # lock으로 동기화 방지
        lock.acquire()
        del self.users[username]
        lock.release()

        self.SendMsgAll('[%s]님이 퇴장했습니다.' %username)
        print('사용자 퇴장: 대화 참여자 수 [%d]' %len(self.users))



   def messageHandler(self, username, msg): # 전송한 msg를 처리하는 부분
        global TimeOverUsers

        if msg.strip() == 'quit': # 유저가 quit 버튼 눌렀을 때
            self.deleteUser(username) # 채팅 종료
            print('사용자 퇴장: 대화 참여자 수 [%d]' %len(self.users))
            return -1
            
        if msg.strip() == 'timeover': # TimeLimit 초과했을 때 채팅 강제 종료
            # self.deleteUser(username)
            # 전역 배열을 만들어서 여기에 username 저장하고,
            # registeruser 부분에서 이 배열에 만약에 저장되어 있는 애면
            # addr만 바꿔줌
            if username not in TimeOverUsers:
                lock.acquire()
                TimeOverUsers.append(username)
                lock.release()
            print('사용자 퇴장: 대화 참여자 수 [%d]' %len(self.users))
            return -2

        elif msg == 'nofile':
            return 3

        elif msg[0] != '/': # 보낸 메세지의 첫문자가 '/'가 아니면
            self.SendMsgAll('[%s] %s' %(username, msg))
            return

        elif msg[0] == '/' and msg[1] == 's' and msg[2] == ' ':
            filename = msg[3:]
            self.SendMsgAll(f'{username}이 파일 server_{filename}를 보냈습니다.')
            return 1

        elif msg[0] == '/' and msg[1] == 'r' and msg[2] == ' ':
            filename = msg[3:]
            self.SendMsgAll(f'{username}이 파일 {filename}를 다운받았습니다.')
            return 2


        
        else:
            self.SendMsgAll('[%s] %s' %(username, msg))
            return
    

   def SendMsgAll(self, msg):  # 채팅방에 접속한 모든 사용자에게 메세지 전달하는 함수
      for conn, addr in self.users.values():
         conn.send(msg.encode())
          

class SocketHandle(socketserver.BaseRequestHandler):
    userman = userHandle()
    
    def handle(self): # 클라이언트가 접속시 클라이언트 주소 출력
        print('[%s] 연결됨' %self.client_address[1])
        global isFalse
        isFalse = True
        global isSame
        isSame = False
        try:
            username = self.registerUsername()
            if username == 'quit': # 유저가 quit 버튼 눌렀을 때
                self.request.send('채팅이 종료되었습니다.\n'.encode())
                self.request.close()
            elif username == 'false': # username이 이미 등록한 이름일 때
                self.request.close()
            else:
                msg = self.request.recv(1024)
                while msg:
                    x = self.userman.messageHandler(username, msg.decode())
                    if x == -1 or x == -2: # 채팅 종료하는 경우
                        if x == -1: # 유저가 quit 버튼 눌렀을 때
                            self.request.send('채팅이 종료되었습니다.\n'.encode())
                            self.request.close()
                        else: # 유저가 시간 초과되어 강제종료 될 때
                            self.request.send('시간이 초과되었습니다'.encode())
                            self.userman.SendMsgAll('[%s]님의 연결이 끊어졌습니다.\n' %username)
                            self.request.close()        
                        break
                    elif x == 1:
                        filename = msg.decode()
                        filename = filename[3:]
                        self.getfilefromclient(filename)
                    
                    
                    elif x == 2:
                        filename = msg.decode()
                        filename = filename[3:]
                        self.sendfiletoclient(filename, username)

                    elif x == 3:
                        sendnofile = '그 파일은 존재하지 않습니다.'
                        self.request.send(sendnofile.encode())
                    
                    msg = self.request.recv(1024)
                    print(msg.decode())
                    
        except Exception as e:
            print(e)
            self.userman.deleteUser(username)

        print('[%s] 접속종료' %self.client_address[1])
        # self.userman.deleteUser(username)

    def registerUsername(self):
        while True:
            global isFalse
            username = self.request.recv(1024)
            username = username.decode().strip()
            arr = username.split(' ')
            username = arr[0]
            password = arr[1]
            # 클라이언트로 부터 온 이름과 비밀번호 분리

            if self.userman.addUser(username, int(password), self.request, self.client_address):
                return username
            if isFalse:
                return 'false'
            if isSame:
                return 'false'

    def getfilefromclient(self, fn):
        filename = fn
        msg = self.request.recv(1024)
        msg = msg.decode()
        filesize = int(msg)
        with open(f'server_{filename}', 'wb') as f:
            try:
                data = self.request.recv(filesize)
                f.write(data)
            except Exception as e:
                print(e)
        return

    def sendfiletoclient(self, fn, un):
        username = un
        filename = fn
        sendmsg = 'filestart'
        self.request.send(sendmsg.encode())
        time.sleep(0.5)
        filesize = str(getsize(filename))
        fileinfo = f'{filename}/{filesize}/{username}'
        fileinfo = fileinfo.encode()
        filesize = int(filesize)
        self.request.send(fileinfo)
        time.sleep(0.5)
        with open(f'{filename}', 'rb') as f:
            try:
                data = f.read(filesize)
                self.request.send(data)
            except Exception as e:
                print(e)
        return

class MakeServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
        


if __name__ == '__main__':
    HOST = input("IP 주소를 입력하세요: ")
    PORT = input("port 번호를 입력하세요: ")
    PASS = input("password를 입력하세요: ")
    PASSWORD = int(PASS)
    # ip, port, name, password 초기값 설정 

    print("run server")
    try:
        server= MakeServer((HOST, int(PORT)), SocketHandle)
        server.serve_forever()
    except KeyboardInterrupt: #ctrl+c 누르면 서버 종료
        print("stop server")
        server.shutdown()
        server.server_close()

        
