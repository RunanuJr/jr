from getpass import getpass
username = input("Enter your username: ")
password = getpass("Enter your password: ")

print(f"Username: {username}")
print(f"Password: {'*' * len(password)}")