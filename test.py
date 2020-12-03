import socketserver
from os.path import exists, getsize

import threading
HOST = ''
PORT = 9009




lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성
class UserManager:
	def __init__(self):
		self.users = {} 	# 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}

	def addUser(self, username, conn, addr): # 사용자 ID를 self.users에 추가하는 함수
		if username in self.users:
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

	def messageHandler(self, username, msg): # 전송한 msg를 처리하는 부분
		if msg[0] != '/': # 보낸 메세지의 첫문자가 '/'가 아니면
			self.sendMessageToAll('[%s] %s' %(username, msg))
			
			return
		if msg.strip() == '/quit': # 보낸 메세지가 'quit'이면
			self.removeUser(username)
			return -1
		# client send to server
		if msg[0] == '/' and msg[1] == 's' and msg[2] == ' ':
			msg_ = msg[3:]
			self.sendMessageToAll(f'{username}이 파일 {username}_download_{msg_}를 보냈습니다.')
			return 2


		# client get from server

		if msg[0] == '/' and msg[1] == 'r' and msg[2] == ' ':
			msg_ = msg[3:]
			# self.sendMessageToAll(f'{username}이 파일 server_{msg_}을 다운받았습니다.')
			return 1
			
		

	
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
				messagetype = self.userman.messageHandler(username, msg.decode())
				if messagetype == -1:
					self.request.close()
					break
				if messagetype == 1:
					msg = msg.decode()
					msg = msg[3:]
					self.sendfiletoclient(msg)

				if messagetype == 2:
					msg = msg.decode()
					msg = msg[3:]
					self.getfilefromclient(msg)

				msg = self.request.recv(1024)

		except Exception as e:
			print(e)
		print('[%s] 접속종료' %self.client_address[0])
		self.userman.removeUser(username)

	def registerUsername(self):
		while True:
			self.request.send('로그인ID:'.encode())
			username = self.request.recv(1024)
			username = username.decode().strip()
			if self.userman.addUser(username, self.request, self.client_address):
				return username

	def Username(self):
		self.request.send('ID:'.encode())
		username = self.request.recv(1024).decode()
		return username

	def sendfiletoclient(self, MSG):
		data_transferred = 0
		filename = MSG
		
		if not exists(filename): # 파일이 해당 디렉터리에 존재하지 않으면
			return # 함수를 빠져 나온다.
		filesize = str(getsize(filename))
		name = self.Username()
		fileinfo = f'{filename}/{filesize}/{name}'
		self.request.send('filestart'.encode())
		self.request.send(fileinfo.encode())
		print('파일[%s] 전송 시작...' %filename)
		with open(filename, 'rb') as f:
			try:
				data = f.read(int(filesize)) # 파일을 파일사이즈만큼 읽음
				self.request.send(data)
				data_transferred = getsize(filename)
			except Exception as e:
				print(e)

		print('전송완료[%s], 전송량[%d]' %(filename,data_transferred))
		# self.request.send('data_transferred'.encode())
		return

	def getfilefromclient(self, MSG):
		filename = MSG
		filesize = int(self.request.recv(1024).decode())
		
		data = self.request.recv(filesize)
		if not data:
				print('파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' %filename)
				return
		with open(f'server_{filename}', 'wb') as f:
				try:
						f.write(data)
				except Exception as e:
					 print(e)

		return

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