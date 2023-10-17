import bcrypt
from datetime import datetime
from datetime import timedelta
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
                if self.check_username == username:
                    # Verify the password using the stored salt
                    if bcrypt.checkpw(self.check_password.encode(), stored_password.encode()):
                        print(f"Hello {username}, Welcome to CarParkBooking")
                        return True
            print("Your password or username is incorrect")
            return False

# Reservation
class Reservation:
    def __init__(self, username):
        self.username = username
        self.date = None
        self.time = None
        self.duration = None

    def is_valid_date(self):
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def is_valid_time(self):
        try:
            time_format = "%H:%M"
            valid_start_time = datetime.strptime("10:00", time_format)
            valid_end_time = datetime.strptime("21:00", time_format)
            user_time = datetime.strptime(self.time, time_format)

            return valid_start_time <= user_time <= valid_end_time
        except ValueError:
            return False

    def is_valid_duration(self):
        return 1 <= self.duration <= 11  # Assuming a valid duration range of 1-11 hours

class ReservationSystem:
    def __init__(self):
        self.reservations_file = "reservations.txt"

    def make_reservation(self, username):
        reservation = Reservation(username)
        while True:
            reservation.date = input("Fill in your desired date (YYYY-MM-DD): ")
            if not reservation.is_valid_date():
                print("Invalid date input")
                continue

            reservation.time = input("Enter your time (starting from 10:00 - 21:00): ")
            if not reservation.is_valid_time():
                print("Invalid time input")
                continue

            while True:
                duration_input = input("Enter the duration of your parking (1-11 hours): ")
                try:
                    reservation.duration = int(duration_input)
                    if not reservation.is_valid_duration():
                        print("Invalid duration input. Duration should be between 1 and 11 hours.")
                    else:
                        break
                except ValueError:
                    print("Invalid duration input. Please enter a valid number.")

            if self.is_slot_available(reservation.date, reservation.time, reservation.duration):
                self.save_reservation(reservation)
                print("Reservation successfully made.")
                break
            else:
                print("The selected slot is not available. Please choose a different date, time, or duration.")

    def is_slot_available(self, date, time, duration):
        with open(self.reservations_file, "r") as file:
            reservations = file.readlines()
            for reservation in reservations:
                parts = reservation.split()
                if date == parts[1] and time == parts[2]:
                    return False
        return True

    def save_reservation(self, reservation):
        with open(self.reservations_file, "a") as file:
            file.write(f"{reservation.username} {reservation.date} {reservation.time}-{(datetime.strptime(reservation.time, '%H:%M') + timedelta(hours=reservation.duration)).strftime('%H:%M')}\n")
    
    def fetch_user_reservations(self, username):
        user_reservations = []
        with open(self.reservations_file, "r") as file:
            for line in file:
                parts = line.split()
                if parts[0] == username:
                    user_reservations.append((parts[1], parts[2]))
        return user_reservations

# main code
print("Hello, Welcome to CarParkBooking")
choice = input("Do you already have an account? (yes or no): ")
while True:
    if choice.upper().strip() == "YES":
        login = LogIn()
        if login.check():
            break
    elif choice.upper().strip() == "NO":
        signin = Register()
        signin.create_account()
        break
    else:
        print("Only Yes or No is required")
        choice = input("Do you already have an account? (yes or no): ")
        continue

print("Appreciate your presence today")

if login:
    reservation_system = ReservationSystem()
    reservation_system.make_reservation(login.check_username)

    # Fetch and display user reservations
    user_reservations = reservation_system.fetch_user_reservations(login.check_username)
    if user_reservations:
        print(f"Your reservations:")
        for i, (date, time) in enumerate(user_reservations, start=1):
            print(f"Reservation {i}: Date: {date}, Time: {time}")
    else:
        print("You have no reservations.")