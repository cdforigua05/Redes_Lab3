from socket import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()
parser.add_argument("--threads", type=int, default=5, help="Number of clients")

client_connected = 0

def super_task(args, i):
    print("Cliente "+str(i)+" iniciando conexión")
    s = socket()
    s.connect(("192.168.0.12", 8000))
    print("Cliente"+str(i)+ "conectado")
    global client_connected
    client_connected += 1
    if client_connected == args.threads:
        s.sendall(b'Start transmision OK')



def main(args):
    executor = ThreadPoolExecutor(max_workers=args.threads)
    for i in range(args.threads):
        executor.submit(super_task,args, i)
        
        

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
