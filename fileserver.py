import socketserver
from os.path import exists, getsize
import threading
HOST = ''
PORT = 9000
import time

# class MyTcpHandler(socketserver.BaseRequestHandler):
# 	def handle(self):

# 		data_transferred = 0
          
# 		print('[%s] 연결됨' %self.client_address[0])

# 		filename = self.request.recv(1024) # 클라이언트로 부터 파일이름을 전달받음
# 		if not exists(filename): # 파일이 해당 디렉터리에 존재하지 않으면
# 		 return # handle()함수를 빠져 나온다.

# 		print('파일[%s] 전송 시작...' %filename)
# 		with open(filename, 'rb') as f:
# 			try:
# 				data = f.read(1024) # 파일을 1024바이트 읽음
# 				while data: # 파일이 빈 문자열일때까지 반복
# 					data_transferred += self.request.send(data)
# 					data = f.read(1024)
# 			except Exception as e:
# 				print(e)

# 		print('전송완료[%s], 전송량[%d]' %(filename,data_transferred))


# def runServer():
# 	print('++++++파일 서버를 시작++++++')
# 	print("+++파일 서버를 끝내려면 'Ctrl + C'를 누르세요.")

# 	try:
# 		server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)
# 		server.serve_forever()
# 	except KeyboardInterrupt:
# 		print('++++++파일 서버를 종료합니다.++++++')


# runServer()





lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성

class UserManager: # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스
                    # ① 채팅 서버로 입장한 사용자의 등록
                    # ② 채팅을 종료하는 사용자의 퇴장 관리
                    # ③ 사용자가 입장하고 퇴장하는 관리
                    # ④ 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송

    def __init__(self):
        self.users = {} # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}
    def addUser(self, username, conn, addr): # 사용자 ID를 self.users에 추가하는 함수
        if username in self.users: # 이미 등록된 사용자라면
            conn.send('이미 등록된 사용자입니다.\n'.encode())
            return None
        # 새로운 사용자를 등록함
        lock.acquire() # 스레드 동기화를 막기위한 락
        self.users[username] = (conn, addr)
        lock.release() # 업데이트 후 락 해제

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
        return


    def messageHandler(self, username, msg): # 전송한 msg를 처리하는 부분
        if msg[0] != '/': # 보낸 메세지의 첫문자가 '/'가 아니면
            self.sendMessageToAll('[%s] %s' %(username, msg))
            return
        elif msg.strip() == '/quit': # 보낸 메세지가 'quit'이면
            self.removeUser(username)
            return -1
        # client send to server
        elif msg[0] == '/' and msg[1] == 's' and msg[2] == ' ':
            msg = msg[3:]
            self.sendMessageToAll(f'{username}이 파일 {msg}를 보냈습니다.')
            # self.sendfiletoserver(self)
            return 1

        # client get from server
        elif msg[0] == '/' and msg[1] == 'r' and msg[2] == ' ':
            return 2

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())



class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()
    def handle(self): # 클라이언트가 접속시 클라이언트 주소 출력
        print('[%s] 연결됨' %self.client_address[0])

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                x = self.userman.messageHandler(username, msg.decode())
                if  x == -1:
                    self.request.close()
                    break
                #receive from client
                elif x == 1:
                    filename = msg.decode()
                    filename = filename[3:]
                    self.getfilefromclient(filename)
                    #send to client
                elif x == 2:
                    filename = msg.decode()
                    filename = filename[3:]
                    self.sendfiletoclient(filename, username)
                    

                msg = self.request.recv(1024)
                     
        except Exception as e:
            print(e)

        print('[%s] 접속종료' %self.client_address[0])
        self.userman.removeUser(username)

    def getfilefromclient(self, fn):

        data_transferred = 0
        filename = fn
        msg = self.request.recv(1024)
        msg = msg.decode("utf-8", "ignore")
        filesize = int(msg)

        with open(f'server_{filename}', 'wb') as f:
            try:
                data = self.request.recv(filesize)
                f.write(data)
            except Exception as e:
                print(e)

        print(f'수신완료{filename}, 수신량{filesize}')
        return

    def sendfiletoclient(self, fn, un):
        username = un
        filename = fn
        sendmsg = 'filestart'
        self.request.send(sendmsg.encode())
        time.sleep(0.5)
        filesize = str(getsize(filename))
        fileinfo = f'{filename}/{filesize}/{username}'
        print(fileinfo)
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
        print(f'발신완료{filename}, 발신량{filesize}')
        return

    def registerUsername(self):
        while True:
            self.request.send('로그인ID:'.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.addUser(username, self.request, self.client_address):
                return username

class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
        
def runServer():
    print('+++ 채팅 서버를 시작합니다.')
    print('+++ 채텅 서버를 끝내려면 Ctrl-C를 누르세요.')

    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('--- 채팅 서버를 종료합니다.')
        server.shutdown()
        server.server_close()

runServer()