import tkinter as tk
from tkinter import messagebox

class ReservationSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ReservationChecking")
        self.root.geometry("300x150")  # Adjusted the window size
        self.root.resizable(height=False, width=False)

        # Username entry
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack(pady=7)

        # Adjusted the height of the entry widget
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.username_entry.pack(pady=1)

        # Button to check reservation
        self.check_button = tk.Button(self.root, text="Check Reservation", command=self.check_reservation, width=13)
        self.check_button.pack(pady=5)

        # Clear button
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_entry, width=13)
        self.clear_button.pack(pady=1)

        # Result label
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

    def check_reservation(self):
        username = self.username_entry.get()
        with open(reservations_file, "r") as reservation:
            bookings_found = []
            for line in reservation:
                parts = line.split()
                name = parts[0]
                date = parts[1]
                time = parts[2][:2] + ":00"
                duration = len(parts[2].split(","))
                slot = parts[3]
                if name == username:
                    booking_found = f"Username: {name}\nDate: {date}\nStarting time: {time}\nDuration: {duration}\nSlot: {slot}"
                    bookings_found.append(booking_found)

            if bookings_found:
                result_text = "\n\n".join(bookings_found)
                self.show_message("Bookings Found", result_text)
                self.result_label.config(text=result_text)
            else:
                self.show_message("Booking Not Found", "There is no booking with this username")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)
    
    def clear_entry(self):
        self.username_entry.delete(0, 'end')  # Clear the username entry
        self.result_label.config(text="")  # Clear the result label

if __name__ == "__main__":
    reservations_file = "reservations.txt"

    root = tk.Tk()
    app = ReservationSystemGUI(root)
    root.mainloop()
