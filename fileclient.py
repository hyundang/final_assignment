import socket
from threading import Thread
from os.path import exists, getsize
import time


HOST = 'localhost'
PORT = 9000

def sendFileToServer(sock, msg):
	filename = msg[3:]
	if not exists(filename): # 파일이 해당 디렉터리에 존재하지 않으면
			return # 함수를 빠져 나온다.
	print(msg)
	sock.send(msg.encode())
	time.sleep(0.5)
	filesize = getsize(filename)
	print(filesize)
	filesize = str(filesize)
	sock.send(filesize.encode())
	time.sleep(0.5)

	with open(filename, 'rb') as f:
		try: 
			data = f.read(int(filesize))
			sock.send(data)
		except Exception as e:
			print(e)
		
		# print('전송완료[%s], 전송량[%s]' %(filename,filesize))


def getFileFromServer(sock, filename):
		
	 sock.sendall(filename.encode())




def rcvMsg(sock):
		while True:
				try:
					data = sock.recv(1024)
					print('데이타ㅏㅏㅏㅏㅏㅏㅏㅏㅏ' + data.decode())
					if not data:
							break
					if(data.decode().strip() == 'filestart'):
						print('들어옴')
						fileinfo = sock.recv(1024).decode()
						fileinfo = fileinfo.split('/')
						filename = fileinfo[0]
						filesize = int(fileinfo[1])
						username = fileinfo[2]
						print(fileinfo)
						
						with open(f'{username}_download_{filename}', 'wb') as f:
							try:
								data = sock.recv(filesize)
								f.write(data)
								
							except Exception as e:
									print(e)
					else:
						print(data.decode())
						 
				except:
						pass


def runChat():
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				sock.connect((HOST, PORT))
				t = Thread(target=rcvMsg, args=(sock,))
				t.daemon = True
				t.start()

				while True:
						msg = input()
						if msg == '/quit':
							sock.send(msg.encode())
							break
						if msg[0] == '/' and msg[1] == 's' and msg[2] == ' ':
							print('sss')
							sendFileToServer(sock, msg)
							continue

						if msg[0] == '/' and msg[1] == 'r' and msg[2] == ' ':
							print('rrr')
							getFileFromServer(sock, msg)
							continue
						else:
							print('nono')
							sock.send(msg.encode())
							continue
	 
	 
runChat()

