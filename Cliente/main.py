import hashlib
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

SIZE = 1024
cn=1
FORMAT = "utf-8"
parser = argparse.ArgumentParser()
parser.add_argument("--threads", type=int, default=cn, help="Number of clients")

client_connected = 0


def super_task(args, i):
    print("Cliente "+str(i)+" iniciando conexión")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8000))
    print("Cliente"+str(i)+ "conectado")
    global client_connected
    client_connected += 1
    if client_connected == args.threads:
        s.send('Start transmision OK'.encode(FORMAT))
        filename = "Cliente"+str(i)+"-Prueba-"+str(cn)

        dataHash = s.recv(SIZE).decode(FORMAT)
        print(str(i)+"hash:"+dataHash)
        data = s.recv(SIZE).decode(FORMAT)
        dataEn= data.encode(FORMAT)
        print(str(i)+"Data:"+data)
        vhash = hashlib.md5(dataEn).hexdigest()
        print(str(i)+"vhash:"+vhash)
        if vhash==dataHash:
            file = open(filename, "w")
            file.write(data)
            file.close()
        else:
            print("hash incorrecto")
            s.send("hash incorrecto".encode(FORMAT))        

        s.close()



def main(args):
    executor = ThreadPoolExecutor(max_workers=args.threads)
    for i in range(args.threads):
        executor.submit(super_task,args, i)
        
        

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
