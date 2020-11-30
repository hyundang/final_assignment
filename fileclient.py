import socket
from threading import Thread

HOST = 'localhost'
PORT = 9009

def sendFileToServer(filename):
   data_transferred = 0

   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      sock.connect((HOST,PORT))
      sock.sendall(filename.encode())

      data = sock.recv(1024)
      if not data:
         print('파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' %filename)
         return

      with open('D:/final_assignment1/download/download' + filename, 'wb') as f:
         try:
            while  data:
               f.write(data)
               data_transferred += len(data)
               data = sock.recv(1024)
         except Exception as e:
            print(e)

   print('파일[%s] 전송종료. 전송량 [%d]' %(filename, data_transferred))


def getFileFromServer(filename):
    
    filename = input('다운로드 받을 파일이름을 입력하세요:')
    getFileFromServer(filename)

   data_transferred = 0

   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      sock.connect((HOST,PORT))
      sock.sendall(filename.encode())

      data = sock.recv(1024)
      if not data:
         print('파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' %filename)
         return

      with open('D:/final_assignment1/download/download' + filename, 'wb') as f:
         try:
            while  data:
               f.write(data)
               data_transferred += len(data)
               data = sock.recv(1024)
         except Exception as e:
            print(e)

   print('파일[%s] 전송종료. 전송량 [%d]' %(filename, data_transferred))




def rcvMsg(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
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
            if msg[0] == '/' and msg[1] == 'f' and msg[2] == ' ':
                msg = msg[3:]
                sendFileToServer()


            sock.send(msg.encode())


runChat()