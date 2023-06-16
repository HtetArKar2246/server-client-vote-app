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