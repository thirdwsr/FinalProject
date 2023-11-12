import tkinter as tk
from tkinter import simpledialog, messagebox
import bcrypt
from datetime import datetime
import sys
import calendar


user_file = "users.txt"
reservations_file = "reservations.txt"

class Register:
    def __init__(self):
        self.username = simpledialog.askstring("ezpark", "Create a username:")
        self.password = simpledialog.askstring("ezpark", "Create a password:")

    def create_account(self):
        while True:
            if len(self.password) <= 6:
                messagebox.showerror("ezpark", "Your password is too short")
                self.username = simpledialog.askstring("ezpark", "Create a username:")
                self.password = simpledialog.askstring("ezpark", "Create a password:")
            else:
                with open(user_file, "r") as file:
                    if self.username not in [line.split()[0] for line in file]:
                        hashed_password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
                        with open(user_file, "a") as file:
                            file.write(f"{self.username} {hashed_password.decode()}\n")
                            messagebox.showinfo("ezpark", "Your account is successfully created")
                        break
                    else:
                        messagebox.showerror("ezpark", "Username has been used")
                        self.username = simpledialog.askstring("ezpark", "Create a different username:")
                        self.password = simpledialog.askstring("ezpark", "Create a password:")

class LogIn:
    def __init__(self):
        self.check_username = None
        self.check_password = None

    def check(self):
        while True:
            self.check_username = simpledialog.askstring("ezpark", "Enter a username:")
            if self.check_username is None:
                sys.exit()  # Exit if user clicks "Cancel"
            self.check_password = simpledialog.askstring("ezpark", "Enter a password:")
            if self.check_password is None:
                sys.exit()  # Exit if user clicks "Cancel"
            with open(user_file, "r") as file:
                read = file.readlines()
                for line in read:
                    parts = line.split(" ")
                    username = parts[0]
                    stored_password = parts[1].strip()
                    if self.check_username == username:
                        if bcrypt.checkpw(self.check_password.encode(), stored_password.encode()):
                            messagebox.showinfo("ezpark", f"Hello {username}")
                            return username
                        else:
                            messagebox.showerror("ezpark", "Your password is incorrect")
                            break
                else:
                    messagebox.showerror("ezpark", "Your username is not found")
                    continue

class Reservation:
    def __init__(self, username):
        self.username = username
        self.date = None
        self.time = None
        self.duration = None
        self.available_slot = None
        self.slot = None
        self.store_time = None
        self.price = 50 # 50 baht per hour

    def is_valid_date(self, date):
        try:
            # Parse the input date
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()

            # Get the current date
            current_date = datetime.now().date()

            # Check if the date is not in the past and is a valid future date
            if date_obj >= current_date:
                # Check if the date exists in the calendar
                _, max_days = calendar.monthrange(date_obj.year, date_obj.month)
                if 1 <= date_obj.day <= max_days:
                    return True
                else:
                    return False
            else:
                return False

        except ValueError:
            # If there is a ValueError, it means the date format is incorrect
            return False

    def is_valid_time(self, time):
        try:
            time_obj = datetime.strptime(time, "%H:%M").time()
            return datetime.strptime("10:00", "%H:%M").time() <= time_obj < datetime.strptime("21:00", "%H:%M").time() and time.endswith(":00")
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
            date_input = simpledialog.askstring("ezpark", "Fill in your desired date (YYYY-MM-DD):")
            if date_input is None:
                sys.exit()  # Exit if user clicks "Cancel"
            if self.is_valid_date(date_input):
                self.date = date_input
                break
            else:
                messagebox.showerror("ezpark", "Invalid date input")

    def get_time(self):
        while True:
            time_input = simpledialog.askstring("ezpark", "Enter your time (starting from 10:00 - 21:00):")
            if time_input is None:
                sys.exit()  # Exit if user clicks "Cancel"
            if self.is_valid_time(time_input):
                self.time = time_input
                break
            else:
                messagebox.showerror("ezpark", "Invalid time input")

    def get_duration(self):
        while True:
            duration_input = simpledialog.askstring("ezpark", "Duration of your parking (1-11):")
            if duration_input is None:
                sys.exit()  # Exit if user clicks "Cancel"
            if self.is_valid_duration(duration_input):
                self.duration = int(duration_input)
                time_num = int(self.time[:2])
                self.store_time = [time_num + i for i in range(self.duration)]
                if self.store_time[-1] >= 22:
                    messagebox.showerror("ezpark", "Parking duration exceeds closing time (22:00)")
                    return False
                break
            else:
                messagebox.showerror("ezpark", "Invalid duration input")

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
                messagebox.showinfo("ezpark", "All slots are booked")
            else:
                messagebox.showinfo("ezpark", f"Available slots are: {', '.join(map(str, self.available_slot))}")

    def get_slot(self):
        while True:
            picked_slot = simpledialog.askinteger("ezpark", "Choose your slot:", minvalue=1, maxvalue=15)
            if picked_slot is None:
                sys.exit()  # Exit if user clicks "Cancel"
            if picked_slot not in self.available_slot or picked_slot > 15 or picked_slot < 1:
                messagebox.showerror("ezpark", "Your picked slot is not valid")
            else:
                self.slot = picked_slot
                break
        global total_price
        total_price = self.duration*self.price

    def store_informations(self):
        with open(reservations_file, "a") as file:
            times_str = ",".join(map(str, self.store_time))
            file.write(f"{self.username} {self.date} {times_str} {self.slot} {self.duration*self.price}\n")

# Main code
root = tk.Tk()
root.withdraw()

messagebox.showinfo("ezpark", "Welcome to ezpark")

choice = simpledialog.askstring("ezpark", "Do you already have an account? (yes or no):")
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
        messagebox.showerror("ezpark", "Only Yes or No is required")
        choice = simpledialog.askstring("ezpark", "Do you already have an account? (yes or no):")
        continue

messagebox.showinfo("ezpark", "Appreciate your presence today")

total_price = 0
if username is not None:
    reservation = Reservation(username)
    reservation.get_date()
    reservation.get_time()
    while reservation.get_duration() == False:
        ask = simpledialog.askinteger("ezpark", "1. Exit\n2. Try again", minvalue=1, maxvalue=2)
        if ask == 1:
            messagebox.showinfo("ezpark", "We hope to see you again")
            sys.exit()  # Exit if user clicks "Cancel"
        else:
            reservation.get_date()
            reservation.get_time()
    reservation.check_availability()
    reservation.get_slot()
    price_ask = messagebox.askyesno("ezpark", "Your total payment is {} baht. Do you want to proceed?".format(total_price), icon=messagebox.INFO)
    if price_ask == 'yes':
        reservation.store_informations()
        messagebox.showinfo("ezpark", "Your booking is done. Thank you for choosing CarParkBooking")
    else:
        messagebox.showinfo("ezpark", "We hope to see you again")
else:
    messagebox.showerror("ezpark", "Login information not available")

root.mainloop()
