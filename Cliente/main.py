import hashlib
from os import set_inheritable
import socket
from socket import error
import argparse
from threading import Thread
from datetime import date, datetime
import os
import threading
import time
SIZE = 2048
cn=5
FORMAT = "utf-8"
parser = argparse.ArgumentParser()
parser.add_argument("--threads", type=int, default=cn, help="Number of clients")
parser.add_argument("--file_id",type=int, choices=[1,2], default=1, help="1 for 100MB file, 2 for 250 MB file")

client_connected = 0

class Client(Thread):
    def __init__(self, i, logger, lock):
        Thread.__init__(self)
        self.i = i
        self.logger = logger
        self.lock = lock
    def run(self):
        print("Cliente "+str(self.i)+" iniciando conexión")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 9879))
        print("Cliente "+str(self.i)+ " conectado")
        
        s.send('Start transmision OK'.encode(FORMAT))
        filename = "ArchivosRecibidos/Cliente"+str(self.i)+"-Prueba-"+str(args.threads)
        sizefile = s.recv(SIZE).decode(FORMAT)
        dataHash = s.recv(SIZE).decode(FORMAT)
        print(str(self.i)+"hash:"+dataHash)
        data = ""
        i=0
        time_inicio = time.time()
        paquetes = 0
        bytes_enviados = 0
        while True:
            try:
                input_data = s.recv(SIZE).decode(FORMAT)
                paquetes+=1
            except error:
                print ("Error de lectura")
                break
            else:
                if input_data:
                    # Compatibilidad con Python 3.
                    if input_data.endswith("Termino:200"):
                        data+=input_data.replace("Termino:200","")
                        bytes_enviados+=len(input_data.replace("Termino:200",""))
                        break
                    else:
                        # Almacenar datos.
                        data+=input_data
                        bytes_enviados+=len(input_data)
                        
        print("Archivo recibido por completo en el cliente", self.i)
        time_final = time.time()
        contenido_output = ""
        contenido_output += "Tamanio archivo: "+str(sizefile)+"\n"
        contenido_output +="Tiempo de transferencia"+str(self.i)+" es "+ str(time_final-time_inicio)+"\n"
        contenido_output += "Paquetes recibidos por el cliente "+str(self.i)+" son "+ str(paquetes)+"\n"
        contenido_output += "Bytes recibidos por el cliente "+str(self.i)+" son "+ str(bytes_enviados)+"\n"
        #data = s.recv(SIZE).decode(FORMAT)
        #print(str(self.i)+"Data:"+data)
        data= data.encode(FORMAT)
        vhash = hashlib.md5(data).hexdigest()
        print(str(self.i)+"vhash:"+vhash)
        print(str(self.i)+"dataHash:"+dataHash)
        if vhash==dataHash:
            file = open(filename, "wb")
            file.write(data)
            file.close()
            print("hash correcto cliente "+str(self.i))
            contenido_output += "Archivo recibido correctamente por cliente "+str(self.i)+"\n"
            s.send(("hash correcto cliente "+str(self.i)).encode(FORMAT))
        else:
            print("hash incorrecto cliente "+str(self.i))
            contenido_output +="Archivo NO recibido correctamente por cliente"+str(self.i)+"\n"
            s.send(("hash correcto cliente "+str(self.i)).encode(FORMAT))        
        contenido_output+="\n"
        self.lock.acquire()
        self.logger.write(contenido_output)
        self.lock.release()
        s.close()



def main(args):
    fecha = datetime.now()
    date_time = fecha.strftime("%m-%d-%Y-%H-%M-%S")
    log = open("logs/"+date_time+"-log.txt", "w")
    if args.file_id==1:
        file_name = "100.txt"
    else:
        file_name = "250.txt"
    log.write("Nombre archivo: "+ file_name+"\n")
    for i in range(args.threads):
        lock = threading.Lock()
        c=Client(i,log, lock)
        c.start()      
        

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
