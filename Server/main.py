from abc import abstractmethod
from socket import socket, error
from threading import Thread
import hashlib
import pickle
import logging
from datetime import date, datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file",type=int, choices=[1,2], help="1 for 100MB file, 2 for 250 MB file")
parser.add_argument("--threads", type=int, help= "Number of clients")


class Server(Thread):
    def __init__(self, conn, addr, logger):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.logger
    def run(self):
        hasher = hashlib.md5()
        while True:
            try:
                input_data = self.conn.recv(1024)
            except error:
                print("Error de lectura")
                break
            else:
                if input_data==1:
                    file_name = "./data/100.txt"
                else:
                    file_name = "./data/250.txt"
                with open(file_name, "rb") as f:
                    buf = f.read()
                    hasher.update(buf)
                    codigo_hash = hasher.hexdigest()
                    self.conn.send("Hash:"+ str(codigo_hash))
                    #content = f.read(1024)
                    #while content:
                    #    self.conn.send(content)
                    #    content = f.read(1024)

                break
def main(args):
    s =socket()
    s.bind(("localhost",8000))
    s.listen(25)
    fecha = datetime.now()
    date_time = fecha.strftime("%m-%d-%Y-%H-%M-%S")
    logger = logging.getLogger(date_time+"")
    logger.setLevel(logging.INFO)
    logger.info("Prueba"+date_time)
    #TODO Revisar conexiones
    connections = []
    while len(connections)!=args.threads:
        conn, addr = s.accept()
        print("Conectado con", addr)
        connections.append((conn, addr))
        #c = Server(conn, addr, logger)
        #c.start()
        #print("Se ha conectado a", addr)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
