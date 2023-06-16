import socket

class TCPclient():
    def __init__(self):
        self.ip = "localhost"
        self.port = 9997

    def run_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.ip, self.port))
        return client

    def main_menu(self):
        self.client = self.run_client()
        reply = self.client.recv(1024).decode("utf-8")
        print(reply)
        try:
            command:str = input("Enter Command: ")
            self.client.send(bytes(command,"utf-8"))
            process,reply = self.client.recv(1024).decode("utf-8").split("||")
            print(reply)
            if process == "1":
                self.register()
            elif process == "2":
                pass
            elif process == "3":
                pass
        except Exception as err:
            print(err)

    def register(self):
        reply = self.client.recv(1024).decode("utf-8")
        print(reply)
        command: str = input("Enter Command: ")
        self.client.send(bytes(command,"utf-8"))
        process, reply = self.client.recv(1024).decode("utf-8").split("||")
        if process == "1":
            print(reply)
            self.voter_register()
        elif process == "2":
            print(reply)

    def voter_register(self):
        email:str = input("Enter Email To Register:")
        result = self.email_checker(email)
        if result ==  1:
            self.client.send(bytes(email, "utf-8"))
        #     continue register
        else:
            print("\nEmail Format Worng!!")
            self.register()

    def email_checker(self,email):
        name_counter = 0
        for i in range(len(email)):
            if email[i] == '@':
                break
            name_counter += 1

        email_name = email[0:name_counter]
        email_form = email[name_counter:]

        name_flag = 0
        email_flag = -1
        domain_form = ["@facebook.com", "@ncc.com", "@mail.ru", "@yahoo.com", "@outlook.com", "@apple.com", "@zoho.com",
                       "@gmail.com"]
        for i in email_name:
            if (31 < ord(i) < 48) or (57 < ord(i) < 65) or (90 < ord(i) < 97) or (122 < ord(i) < 128):
                name_flag = -1
                break

        for i in domain_form:
            if email_form == i:
                email_flag = 0
                break

        if name_flag == -1 or email_flag == -1:
            return -1

        else:
            return 0


if __name__ == "__main__":
    while True:
        client = TCPclient()
        client.main_menu()