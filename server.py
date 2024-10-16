import socket
import pymongo
import hashlib

connection = pymongo.MongoClient("localhost", 27017)
db = connection['vote_app']
users_collection = db['users']
candidates_collection = db['candidates']


class TCPserver:
    def __init__(self):
        self.server_ip = "localhost"
        self.server_port = 8080

    def main(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen()
        print("Server listening on port: {} and IP: {}".format(self.server_port, self.server_ip))
        try:
            while True:
                client, address = server.accept()
                print("Accepted connection from {}:{}".format(address[0], address[1]))
                self.handle_client(client)
        except Exception as err:
            print("Error: ", err)

    def handle_client(self, client_socket):
        with client_socket as sock:
            request = sock.recv(1024).decode("utf-8")
            print("Received: {}".format(request))

            if request.startswith("register"):
                self.register(sock, request)
            elif request.startswith("login"):
                self.login(sock, request)
            elif request.startswith("vote"):
                self.vote(sock, request)
            elif request.startswith("view_candidates"):
                self.view_candidates(sock)
            elif request.startswith("admin"):
                self.handle_admin(sock, request)

    def hash_password(self, password):
        """Hashes the password using SHA-256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def register(self, sock, request):
        """Handles user registration for both voters and admins."""
        try:
            _, username, password, role = request.split("|")
            if users_collection.find_one({"username": username}):
                sock.send("User already exists. Please try again.".encode("utf-8"))
                return

            hashed_pw = self.hash_password(password)
            users_collection.insert_one({"username": username, "password": hashed_pw, "role": role, "has_voted": False})
            sock.send("Registration successful.".encode("utf-8"))
        except Exception as err:
            sock.send(f"Registration failed: {err}".encode("utf-8"))

    def login(self, sock, request):
        """Validates user credentials and retrieves user role."""
        try:
            _, username, password = request.split("|")
            user = users_collection.find_one({"username": username})
            if not user:
                sock.send("User does not exist. Please register.".encode("utf-8"))
                return

            hashed_pw = self.hash_password(password)
            if user["password"] == hashed_pw:
                sock.send(f"Login successful|{user['role']}".encode("utf-8"))
            else:
                sock.send("Invalid credentials. Please try again.".encode("utf-8"))
        except Exception as err:
            sock.send(f"Login failed: {err}".encode("utf-8"))

    def view_candidates(self, sock):
        """Allows voters to view the list of candidates."""
        try:
            candidates = list(candidates_collection.find({}))  # Convert cursor to list
            if not candidates:  # Check if the list is empty
                sock.send("No candidates available.".encode("utf-8"))
                return

            result = "Current Candidates:\n"
            for candidate in candidates:
                result += f"{candidate['name']}: {candidate['votes']} votes\n"
            sock.send(result.encode("utf-8"))
        except Exception as err:
            sock.send(f"Failed to retrieve candidates: {err}".encode("utf-8"))

    def vote(self, sock, request):
        """Handles voting by a user for a specific candidate."""
        try:
            _, username, candidate_name = request.split("|")
            user = users_collection.find_one({"username": username})

            if user is None:
                sock.send("User not found. Please login first.".encode("utf-8"))
                return

            if user.get("has_voted"):
                sock.send("You have already voted.".encode("utf-8"))
                return

            candidate = candidates_collection.find_one({"name": candidate_name})
            if candidate:
                candidates_collection.update_one({"name": candidate_name}, {"$inc": {"votes": 1}})
                users_collection.update_one({"username": username}, {"$set": {"has_voted": True}})
                sock.send("Vote successful.".encode("utf-8"))
            else:
                sock.send(f"Candidate {candidate_name} not found.".encode("utf-8"))
        except Exception as err:
            sock.send(f"Voting failed: {err}".encode("utf-8"))

    def handle_admin(self, sock, request):
        """Handles admin actions such as adding/removing candidates."""
        try:
            action, username, *args = request.split("|")
            user = users_collection.find_one({"username": username})

            if user is None or user["role"] != "admin":
                sock.send("Access denied. Admins only.".encode("utf-8"))
                return

            if action == "1":  # Add candidate
                candidate_name = args[0] if args else ""
                candidates_collection.insert_one({"name": candidate_name, "votes": 0})
                sock.send(f"Candidate {candidate_name} added.".encode("utf-8"))

            elif action == "2":  # Remove candidate
                candidate_name = args[0] if args else ""
                result = candidates_collection.delete_one({"name": candidate_name})
                if result.deleted_count > 0:
                    sock.send(f"Candidate {candidate_name} removed.".encode("utf-8"))
                else:
                    sock.send(f"Candidate {candidate_name} not found.".encode("utf-8"))

            elif action == "3":  # View candidates
                candidates = list(candidates_collection.find({}))
                if not candidates:
                    sock.send("No candidates available.".encode("utf-8"))
                    return

                result = "Current Candidates:\n"
                for candidate in candidates:
                    result += f"{candidate['name']}: {candidate['votes']} votes\n"
                sock.send(result.encode("utf-8"))

        except Exception as err:
            sock.send(f"Admin action failed: {err}".encode("utf-8"))


if __name__ == "__main__":
    tcpserver = TCPserver()
    tcpserver.main()
