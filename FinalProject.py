import bcrypt
from datetime import datetime

# Create an account
class Register:
    def __init__(self):
        self.username = input("Create a username: ")
        self.password = input("Create a password: ")

    def create_account(self):
        while True:
            if len(self.password) <= 6:
                print("Your password is too short")
                self.username = input("Create a username: ")
                self.password = input("Create a password: ")
            else:
                with open("users.txt", "r") as file:
                    if self.username not in [line.split()[0] for line in file]:
                        # Hash the password with the generated salt
                        hashed_password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
                        
                        # Append the username, salt, and hashed password to users.txt
                        with open("users.txt", "a") as file:
                            file.write(f"{self.username} {hashed_password.decode()}\n")
                            print("Your account is successfully created")
                        break
                    else:
                        print("Username has been used")
                        self.username = input("Create a different username: ")
                        self.password = input("Create a password: ")

# LogIn process
class LogIn:
    def __init__(self):
        self.check_username = input("Enter a username: ")
        self.check_password = input("Enter a password: ")
    
    def check(self):
        with open("users.txt", "r") as file:
            read = file.readlines()
            for line in read:
                parts = line.split(" ")
                username = parts[0]
                stored_password = parts[1].strip()
            while True:
                if self.check_username == username:
                    # Verify the password using the stored salt
                    if bcrypt.checkpw(self.check_password.encode(), stored_password.encode()):
                        print(f"Hello {username}, Welcome to CarParkBooking")
                        return
                else:
                    print("Your password or username is incorrect")
                    self.check_username = input("Enter a username: ")
                    self.check_password = input("Enter a password: ")
                    continue
# Reservation
class Reservation:
    def __init__(self):
        self.date = input("Fill in your desire date(YYYY-MM-DD): ")
        #self.time = input("Enter your time (starting from 10:00 - 21:00): ")
        #self.duration = int(input("Duration of your parking(1-11): "))
    
    def is_valid_date(self):
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
            return True
        except ValueError:
            return False


# main code
print("Hello, Welcome to CarParkBooking")
choice = input("Do you already have an account?(yes or no): ")
while True:
    if choice.upper().strip() == "YES":
        login = LogIn()
        login.check()
        break
    elif choice.upper().strip() == "NO":
        signin = Register()
        signin.create_account()
        break
    else:
        print("Only Yes or No is required")
        choice = input("Do you already have an account?(yes or no): ")
        continue
print("Appreciate your presence today")
while True:
    book = Reservation()
    if book.is_valid_date() == False:
        print("Invalid date input")
        continue
    else:
        print("SUSU")
        break