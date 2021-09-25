from abc import abstractmethod
import socket
from threading import Thread
import hashlib
import pickle
import logging
from datetime import date, datetime
import argparse

SIZE = 1024
FORMAT = "utf-8"
cn=25
parser = argparse.ArgumentParser()
parser.add_argument("--file",type=int, choices=[1,2], help="1 for 100MB file, 2 for 250 MB file")
parser.add_argument("--threads", type=int, default=cn, help= "Number of clients")

class Server(Thread):
    def __init__(self, conn, addr, logger):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.logger=logger
    def run(self):
        input_data=self.conn.recv(SIZE).decode(FORMAT)
        print(input_data)
        if input_data==1:
            file_name = "./data/100.txt"
        else:
            file_name = "./data/250.txt"
        file = open(file_name, "r")
        data = file.read()
        dataEn=data.encode(FORMAT)
        dataHash = hashlib.md5(dataEn).hexdigest()
        self.conn.send(dataHash.encode(FORMAT))
        self.conn.send(dataEn)
        file.close()
        self.conn.close()

def main(args):
    s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost",9879))
    s.listen(cn)
    fecha = datetime.now()
    date_time = fecha.strftime("%m-%d-%Y-%H-%M-%S")
    logger = logging.getLogger(date_time+"")
    logger.setLevel(logging.INFO)
    logger.info("Prueba"+date_time)
    connections = []
    while len(connections)!=args.threads:
        conn, addr = s.accept()
        print("Conectado con", addr)
        connections.append((conn, addr))
    for con in connections:
        conn=con[0]
        addr=con[1]
        c = Server(conn, addr, logger)
        c.start()
        print("Se ha conectado a", addr)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
