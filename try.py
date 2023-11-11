import bcrypt
import tkinter as tk
from datetime import datetime
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.font import *

user_file = "users.txt"
reservations_file = "reservations.txt"

# Create an account
class Register:
    def __init__(self, on_success, on_back):
        self.on_success = on_success
        self.on_back = on_back

        self.root = tk.Tk()
        self.root.title("Register")
        self.root.geometry("600x400")

        self.label_username = tk.Label(self.root, text="Create a username:")
        self.label_username.pack()

        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        self.label_password = tk.Label(self.root, text="Create a password:")
        self.label_password.pack()

        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        self.button_register = tk.Button(self.root, text="Register", command=self.create_account)
        self.button_register.pack()

    def create_account(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        while True:
            if len(password) <= 6:
                messagebox.showerror("Error", "Your password is too short")
                self.entry_username.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
                return

            with open(user_file, "r") as file:
                if username not in [line.split()[0] for line in file]:
                    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                    with open(user_file, "a") as file:
                        file.write(f"{username} {hashed_password.decode()}\n")
                        messagebox.showinfo("Success", "Your account is successfully created")

                    # Clear registration content
                    self.label_username.pack_forget()
                    self.entry_username.pack_forget()
                    self.label_password.pack_forget()
                    self.entry_password.pack_forget()
                    self.button_register.pack_forget()

                    # Call the on_success function
                    self.on_success()

                    self.root.destroy()
                    break
                else:
                    messagebox.showerror("Error", "Username has been used")
                    self.entry_username.delete(0, tk.END)
                    self.entry_password.delete(0, tk.END)
                    return
# LogIn process
class LogIn:
    def check(self):
        while True:
            check_username = simpledialog.askstring("Enter a username", "Enter a username:")
            if check_username is None:
                return None  # Exit if user clicks "Cancel"
            check_password = simpledialog.askstring("Enter a password", "Enter a password:")
            if check_password is None:
                return None  # Exit if user clicks "Cancel"
            with open(user_file, "r") as file:
                read = file.readlines()
                for line in read:
                    parts = line.split(" ")
                    username = parts[0]
                    stored_password = parts[1].strip()
                    if check_username == username:
                        if bcrypt.checkpw(check_password.encode(), stored_password.encode()):
                            print(f"Hello {username}, Welcome to ezpark")
                            return username
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

def clear_welcome():
    label_welcome.pack_forget()
    login_button.pack(side="top", pady=(160, 10), anchor="center")
    register_button.pack(side="top", pady=10, anchor="center")

def clear_login_register():
    login_button.pack_forget()
    register_button.pack_forget()

def register_clicked():
    register_gui = Register(on_success=clear_welcome, on_back=clear_welcome)

def login_clicked():
    login = LogIn()
    username = login.check()
    print("to do")

root = Tk()
root.title("ezpark")
root.geometry("600x400")
root.resizable(height=False, width=False)

label_welcome = Label(root, text="Hello, welcome to ezpark")
label_welcome["font"] = ["Lato", 25, "bold"]
label_welcome["fg"] = "white"
label_welcome.pack(pady=180)

login_button = Button(root, text="Login", command=login_clicked, width=15)
register_button = Button(root, text="Register", command=register_clicked, width=15)

# Set a timer to clear content after 5000 milliseconds (5 seconds)
root.after(1000, clear_welcome)

root.mainloop()