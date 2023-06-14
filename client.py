import socket

class User():
    def __init__(self):
        self.ip = "localhost"
        self.port = 9999

    def main(self):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((self.ip,self.port))
        try:
            command = input("Enter Command: ")
            to_send_server = bytes(command, "utf-8")
            client.send(to_send_server)
            recv = client.recv(1024)
            reply = recv.decode()
            if reply == "Well Recived Command!!":
                print(reply)
                self.register(client)
            else:
                print(reply)
        except Exception as err:
             print(err)
    def register(self,sock):
        recv = sock.recv(1024)
        reply = recv.decode()
        email = input(reply)
        to_send_server = bytes(email, "utf-8")
        sock.send(to_send_server)
        recv = sock.recv(1024)
        reply = recv.decode()
        if reply == "Email Has Registered!!":
            print(reply)
            self.main()
        else:
            name = input(reply)
            to_send_server = bytes(name, "utf-8")
            sock.send(to_send_server)
            recv = sock.recv(1024)
            reply = recv.decode()
            print(reply)
if __name__ == "__main__":
    while True:
        app = User()
        app.main()











