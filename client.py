import socket


class TCPclient:
    def __init__(self, sms):
        self.target_ip = "localhost"
        self.target_port = 8080
        self.client_sms = bytes(sms, "utf-8")

    def run_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))
        client.send(self.client_sms)
        received_reply = client.recv(1024).decode("utf-8")
        print("Server Response: ", received_reply)
        client.close()
        return received_reply


if __name__ == "__main__":
    role = None
    username = None

    while True:
        print("\n1: Register\n2: Login\n3: Exit")
        choice = input("Choose an action: ")

        if choice == '1':
            # Register
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            role = input("Enter role (admin/voter): ")

            message = f"register|{username}|{password}|{role}"
            reply = TCPclient(message).run_client()
            print(reply)

        elif choice == '2':
            # Login
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            message = f"login|{username}|{password}"
            reply = TCPclient(message).run_client()

            if "Login successful" in reply:
                role = reply.split('|')[-1]
                print(f"Welcome, {username}. You are logged in as {role}.")

                # Displaying admin options or voting options based on the role
                while True:
                    if role == "admin":
                        print("\n1: View Candidates\n2: Add Candidate\n3: Remove Candidate\n4: Logout")
                        admin_choice = input("Choose an action: ")
                        if admin_choice == '1':
                            message = f"admin|{username}|view|"
                            reply = TCPclient(message).run_client()
                            print(reply)
                        elif admin_choice == '2':
                            candidate_name = input("Enter candidate name: ")
                            message = f"admin|{username}|add|{candidate_name}"
                            reply = TCPclient(message).run_client()
                            print(reply)
                        elif admin_choice == '3':
                            candidate_name = input("Enter candidate name to remove: ")
                            message = f"admin|{username}|remove|{candidate_name}"
                            reply = TCPclient(message).run_client()
                            print(reply)
                        elif admin_choice == '4':
                            print("Logging out...")
                            break
                        else:
                            print("Invalid option. Please choose again.")
                    else:  # If the user is a voter
                        print("\n1: View Candidates\n2: Vote\n3: Logout")
                        user_choice = input("Choose an action: ")
                        if user_choice == '1':
                            message = f"view_candidates|{username}|"
                            reply = TCPclient(message).run_client()
                            print(reply)
                        elif user_choice == '2':
                            candidate_name = input("Enter candidate name to vote for: ")
                            message = f"vote|{username}|{candidate_name}"
                            reply = TCPclient(message).run_client()
                            print(reply)
                        elif user_choice == '3':
                            print("Logging out...")
                            break
                        else:
                            print("Invalid option. Please choose again.")
            else:
                print(reply)

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
