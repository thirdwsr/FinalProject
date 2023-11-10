import bcrypt
from datetime import datetime

user_file = "users.txt"
reservations_file = "reservations.txt"

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
                with open(user_file, "r") as file:
                    if self.username not in [line.split()[0] for line in file]:
                        # Hash the password with the generated salt
                        hashed_password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
                        
                        # Append the username, salt, and hashed password to users.txt
                        with open(user_file, "a") as file:
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
        self.check_username = None
        self.check_password = None
    
    def check(self):
        while True:
            self.check_username = input("Enter a username: ")
            self.check_password = input("Enter a password: ")
            with open(user_file, "r") as file:
                read = file.readlines()
                for line in read:
                    parts = line.split(" ")
                    username = parts[0]
                    stored_password = parts[1].strip()
                    if self.check_username == username:
                        # Verify the password using the stored salt
                        if bcrypt.checkpw(self.check_password.encode(), stored_password.encode()):
                            print(f"Hello {username}, Welcome to CarParkBooking")
                            return username  # Return the username if login is successful
                        else:
                            print("Your password is incorrect")
                            break
                else:
                    print("Your username is not found")
                    continue


# Reservation
class Reservation():
    def __init__(self, username):
        self.username = username
        self.date = None
        self.time = None
        self.duration = None
        self.available_slot = None
        self.slot = None
        self.store_time = None

    def is_valid_date(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def is_valid_time(self, time):
        try:
            time_obj = datetime.strptime(time, "%H:%M").time()
            return datetime.strptime("10:00", "%H:%M").time() <= time_obj <= datetime.strptime("21:00", "%H:%M").time()
        except ValueError:
            return False

    def is_valid_duration(self, duration):
        try:
            duration = int(duration)
            return 1 <= duration <= 11
        except ValueError:
            return False

    def get_date(self):
        while True:
            date_input = input("Fill in your desired date (YYYY-MM-DD): ")
            if self.is_valid_date(date_input):
                self.date = date_input
                break
            else:
                print("Invalid date input")

    def get_time(self):
        while True:
            time_input = input("Enter your time (starting from 10:00 - 21:00): ")
            if self.is_valid_time(time_input):
                self.time = time_input
                break
            else:
                print("Invalid time input")

    def get_duration(self):
        while True:
            duration_input = input("Duration of your parking (1-11): ")
            if self.is_valid_duration(duration_input):
                self.duration = int(duration_input)
                # check duration over operating hours
                time_num = int(self.time[:2])
                self.store_time = [time_num + i for i in range(self.duration)]
                if self.store_time[-1] >= 22:
                    print("Parking duration exceeds closing time (22:00)")
                    return False
                break
            else:
                print("Invalid duration input")

    def check_availability(self):
        time_num = int(self.time[:2])
        self.store_time = [time_num + i for i in range(self.duration)]
        with open(reservations_file, "r") as reservation:
            bookedslots = set()
            for line in reservation:
                parts = line.split()
                if len(parts) == 0:
                    break
                date = parts[1]
                booked_time = [int(x) for x in parts[2].split(",")]
                slot = parts[3]
                if self.date == date:
                    if len(set(self.store_time).intersection(booked_time)) > 0:
                        bookedslots.update(slot)

            total_slot = set(range(1, 16))
            self.available_slot = list(total_slot - set([int(x) for x in bookedslots]))
            if not self.available_slot:
                print("All slots are booked")
            else:
                print("Available slots are:", end=" ")
                print(", ".join(map(str, self.available_slot)))

    def get_slot(self):
        picked_slot = int(input("choose your slot: "))
        while True:
            if picked_slot not in self.available_slot or picked_slot > 15 or picked_slot < 1:
                print("Your picked slot is not valid")
                picked_slot = int(input("choose your slot: "))
                continue
            else:
                self.slot = picked_slot
                break
    
    def store_informations(self):
        with open(reservations_file, "a") as file:
            # Join the list of times as a comma-separated string without spaces
            times_str = ",".join(map(str, self.store_time))
            file.write(f"{self.username} {self.date} {times_str} {self.slot}\n")


# Main code
# LogIn system
print("Hello, Welcome to CarParkBooking")
choice = input("Do you already have an account? (yes or no): ")
username = None
while True:
    if choice.upper().strip() == "YES":
        login = LogIn()
        username = login.check()
        break
    elif choice.upper().strip() == "NO":
        signin = Register()
        signin.create_account()
        login = LogIn()
        username = login.check()
        break
    else:
        print("Only Yes or No is required")
        choice = input("Do you already have an account? (yes or no): ")
        continue
print("Appreciate your presence today")

if username is not None:
    reservation = Reservation(username)
    reservation.get_date()
    reservation.get_time()
    while reservation.get_duration() == False:
        ask = input(f"1. Exit\n2. Try again\n1 or 2:")
        if ask == 1:
            exit()
        else:
            reservation.get_date()
            reservation.get_time()
    reservation.check_availability()
    reservation.get_slot()
    reservation.store_informations()
    print("Your booking is done. Thank you for choosing CarParkBooking")
else:
    print("Error: Login information not available.")
