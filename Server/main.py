from abc import abstractmethod
import socket
from threading import Lock, Thread
import hashlib
import pickle
import logging
from datetime import date, datetime
import argparse
import os
import time
import threading
SIZE = 2048
FORMAT = "utf-8"
FILE_END = "FILE_END"
cn=5
parser = argparse.ArgumentParser()
parser.add_argument("--file_id",type=int, choices=[1,2], default=1, help="1 for 100MB file, 2 for 250 MB file")
parser.add_argument("--threads", type=int, default=cn, help= "Number of clients")

class Server(Thread):
    def __init__(self, conn, addr, logger, file_id, lock, sizefile):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.logger=logger
        self.file_id = file_id
        self.lock = lock
        self.sizefile = sizefile
    def run(self):
        input_data=self.conn.recv(SIZE).decode(FORMAT)
        print(input_data)
        if self.file_id==1:
            file_name = "../Data/10.txt"
        else:
            file_name = "../Data/10.txt"
        file = open(file_name, "r")
        data = file.read()
        dataEn=data.encode(FORMAT)
        dataHash = hashlib.md5(dataEn).hexdigest()
        sf = str(self.sizefile)
        self.conn.send(sf.encode(FORMAT))
        self.conn.send(dataHash.encode(FORMAT))
        print("Hash:",dataHash)
        time_inicio = time.time()
        paquetes = 0
        bytes_enviados =0
        while True:
            file = open(file_name, "rb")
            content_file = file.read(SIZE)
            while content_file:
                self.conn.send(content_file)
                bytes_enviados += len(content_file)
                content_file = file.read(SIZE)
                paquetes+=1
            break
        print("Archivo enviado correctamente")
        self.conn.send("Termino:200".encode(FORMAT))
        recibido = self.conn.recv(SIZE).decode(FORMAT)
        time_final = time.time()
        contenido_output = ""
        contenido_output +="Tiempo de transferencia para cliente "+str(self.addr)+" es "+ str(time_final-time_inicio)+"\n"
        contenido_output += "Paquetes enviado al cliente "+str(self.addr)+" son "+ str(paquetes)+"\n"
        contenido_output += "Bytes enviados al cliente "+str(self.addr)+" son "+ str(bytes_enviados)+"\n"

        print(recibido)
        if not "incorrecto" in recibido:
            contenido_output += "Transferencia exitosa para cliente "+str(self.addr)+"\n"
        else:
            contenido_output +="Transferencia NO exitosa para cliente "+str(self.addr)+"\n"
        contenido_output+="\n"
        self.lock.acquire()
        self.logger.write(contenido_output)
        self.lock.release()
        # self.conn.send(dataEn)
        file.close()
        self.conn.close()

        

def main(args):
    s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost",9879))
    s.listen(cn)
    fecha = datetime.now()
    date_time = fecha.strftime("%m-%d-%Y-%H-%M-%S")
    log = open("logs/"+date_time+"-log.txt", "w")
    if args.file_id==1:
        file_name = "../Data/100.txt"
    else:
        file_name = "../Data/250.txt"
    log.write("Nombre archivo: "+ file_name+"\n")
    sizefile = os.stat(file_name).st_size
    log.write("Tamanio archivo: "+str(sizefile)+"\n")
    connections = []
    while len(connections)!=args.threads:
        conn, addr = s.accept()
        print("Conectado con", addr)
        connections.append((conn, addr))
    for con in connections:
        conn=con[0]
        addr=con[1]
        lock = threading.Lock()
        c = Server(conn, addr, log, args.file_id, lock, sizefile)
        c.start()
        print("Se ha conectado a", addr)
        log.write("Se ha conectado cliente "+str(addr)+"\n")

    

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
