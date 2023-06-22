import socket as soket
import threading as thread

port = 5050
sava = soket.gethostbyname(soket.gethostname())

adrr = (sava,port)
FORMAT = 'utf-8'
DISCONNECT_KEY = 'disconnect'
iplist = []
server = soket.socket(soket.AF_INET,soket.SOCK_STREAM)
server.bind(adrr)

def code4_client(conn,addr):
    print(f'NEW CONNECTION{addr} connected')
    connected = True
    while connected:
        meseg = conn.recv(1048576).decode(FORMAT)
        if meseg == DISCONNECT_KEY:
            connected = False
            print(f'{addr} Disconnected!!')
        elif len(meseg) != 0:
            print(f'{addr}: {meseg}')
        else:
            connected = False
            conn.close()

def accept_client():
    server.listen()
    print(f'LISTENING ON {sava}')
    while True:
       conn, addr= server.accept()
       threada = thread.Thread(target=code4_client,args=(conn,addr))
       threada.start()
       iplist.append(addr)
       print(f'[ACTIVE CONNECTIONS] {thread.activeCount()-1}  CONNECTIONS IP ADRESSES: {iplist}')

print('SERVER IS STARTING.....')
accept_client()