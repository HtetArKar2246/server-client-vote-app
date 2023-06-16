<<<<<<< HEAD
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
=======
import socket
import pymongo

connection = pymongo.MongoClient("localhost",27017)
db = connection["db"]
voter = db["voter"]
candidate  = db["candidate"]
class TCPserver():
    def __init__(self):
        self.ip = "localhost"
        self.port = 9997

    def main(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((self.ip,self.port))
        server.listen()
        print("Server is listening on {}:{}".format(self.ip, self.port))
        try:
            while True:
                client, address = server.accept()
                print("Client {}:{} is connected".format(address[0], address[1]))
                self.handle_client(client)
        except Exception as err:
            print(err)
    def handle_client(self,client_socket):
        try:
            with client_socket as self.sock:
                self.sock.send(bytes("Welcome!!", "utf-8"))
                command = self.sock.recv(1024).decode("utf-8")
                if command == "reg":
                    self.sock.send(bytes("1||Your In Register Process", "utf-8"))
                    self.register()
                elif command == "log":
                    self.sock.send(bytes("2||Well Recv Command", "utf-8"))
                elif command == "stop":
                    self.sock.send(bytes("3||Well Recv Command", "utf-8"))
                else:
                    self.sock.send(bytes("0||Unknown Command", "utf-8"))
        except Exception as err:
            print(err)

    def register(self):
        self.sock.send(bytes("\nreg for voter: 'regv' & reg for candidate: 'regc'", "utf-8"))
        command = self.sock.recv(1024).decode("utf-8")
        if command == "regv":
            self.sock.send(bytes("1||This is register for voters","utf-8"))
            email = self.sock.recv(1024).decode("utf-8")
            result = self.data_checker(email,"email",voter)
            if result == -1:
                self.sock.send(bytes("\nEmail Is Already Registered", "utf-8"))
                self.register()
            elif result == 0:
                pass
        #         continue register

        elif command == "regc":
            self.sock.send(bytes("2||This is register for candidate", "utf-8"))
        else:
            self.sock.send(bytes("0||Unknown Command", "utf-8"))

    def data_checker(self,data,d_name,col):
        result = 0
        db = col.find()
        for i in db:
            if data == i[d_name]:
                result = -1
                break
        return result


if __name__=="__main__":
    server = TCPserver()
    server.main()
>>>>>>> master
