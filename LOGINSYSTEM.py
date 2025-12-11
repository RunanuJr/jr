import json
import os

user_file = "users.json"
if not os.path.exists(user_file):
    with open(user_file, 'w') as f:
        json.dump({}, f)
class user:
    def __init__(self, username, password):
        self.username = username
        self.password = password
class LoginSystem:
    def __init__(self, user_file):
        self.user_file = user_file
        self.users = self.load_users()
    def load_users(self):
        with open(self.user_file, 'r') as f:
            return json.load(f)
    def save_users(self):
        with open(self.user_file, 'w') as f:
            json.dump(self.users, f)
    def register(self, username, password):
        if username in self.users:
            print("Username already exists.")
            return "Registration failed."
        self.users[username] = password
        self.save_users()
        print("Registration successful.")
        return True
    def login(self, username, password):
        if username not in self.users:
            print("Username does not exist.")
            return "Login failed."
        if self.users[username] != password:
            print("Incorrect password.")
            return "Login failed."
        print("Login successful.")
        return True
    def main():
        system = LoginSystem(user_file)
        while True:
            choice = input("Enter 'r' to register, 'l' to login, or 'q' to quit: ")
            if choice == 'r':
                username = input("Enter username: ")
                password = input("Enter password: ")
                system.register(username, password)
            elif choice == 'l':
                username = input("Enter username: ")
                password = input("Enter password: ")
                system.login(username, password)
            elif choice == 'q':
                break
            else:
                print("Invalid choice.")
if __name__ == "__main__":
    LoginSystem.main()