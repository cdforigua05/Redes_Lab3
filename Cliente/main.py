import hashlib
import socket
import argparse
from threading import Thread

SIZE = 1024
cn=25
FORMAT = "utf-8"
parser = argparse.ArgumentParser()
parser.add_argument("--threads", type=int, default=cn, help="Number of clients")

client_connected = 0

class Client(Thread):
    def __init__(self, i):
        Thread.__init__(self)
        self.i = i
    def run(self):
        print("Cliente "+str(self.i)+" iniciando conexión")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 9879))
        print("Cliente"+str(self.i)+ "conectado")
        
        s.send('Start transmision OK'.encode(FORMAT))
        filename = "ArchivosRecibidos/Cliente"+str(self.i)+"-Prueba-"+str(cn)

        dataHash = s.recv(SIZE).decode(FORMAT)
        print(str(self.i)+"hash:"+dataHash)
        data = s.recv(SIZE).decode(FORMAT)
        dataEn= data.encode(FORMAT)
        print(str(self.i)+"Data:"+data)
        vhash = hashlib.md5(dataEn).hexdigest()
        print(str(self.i)+"vhash:"+vhash)
        if vhash==dataHash:
            file = open(filename, "w")
            file.write(data)
            file.close()
        else:
            print("hash incorrecto")
            s.send("hash incorrecto".encode(FORMAT))        

        s.close()



def main(args):
    for i in range(cn):
        c= Client(i)
        c.start()      
        

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
