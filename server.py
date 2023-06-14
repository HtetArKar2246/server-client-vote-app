import socket
import pymongo

class Application():
    def __init__(self):
        self.ip = "localhost"
        self.port = 9999
    def db_connect(self):
        self.connection = pymongo.MongoClient("localhost",27017)
        self.db = self.connection["db"]
        self.col = self.db["user_info"]

    def main(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((self.ip,self.port))
        server.listen()
        print("server is listen on {}:{}".format(self.ip,self.port))
        self.db_connect()
        while True:
            try:
                client,address = server.accept()
                print("Client {}:{} is connected".format(address[0],address[1]))
                self.client_hadling(client)
            except Exception as err:
                print(err)
    def client_hadling(self,client_socket):
        with client_socket as sock:
            recv = sock.recv(1024)
            request = recv.decode("utf-8")
            if request == "reg":
                sock.send(bytes("Well Recived Command!!", "utf-8"))
                self.register(sock)
            else:
                sock.send(bytes("Unknown Command!!","utf-8"))

    def register(self,sock):
        sock.send(bytes("Email: ","utf-8"))
        recv = sock.recv(1024)
        email = recv.decode("utf-8")
        check = self.email_check(email,sock)
        if check == 0:
            sock.send(bytes("Name: ","utf-8"))
            recv = sock.recv(1024)
            name = recv.decode("utf-8")
            db = self.col.find()
            id = 0
            for data in db:
                id = data["_id"]
            id+=1
            self.col.insert_one({"_id":id ,"email": email, "name": name})
            sock.send(bytes("Registration successful!", "utf-8"))
        elif check == 1:
            sock.send(bytes("Email Has Registered!!","utf-8"))

    def email_check(self,email,sock):
        if self.col.find_one({"email": email}):
            return 1
        return 0

if __name__ == "__main__":
    app = Application()
    app.main()