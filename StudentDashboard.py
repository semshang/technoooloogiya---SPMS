import tkinter as tk
from tkinter import messagebox
import os

class StudentDashboard:
    def __init__(self, username, fullname):
        self.username = username
        self.fullname = fullname
        self.root = tk.Tk()
        self.root.title("Student Dashboard")
        self.root.geometry("450x400")

        tk.Label(self.root, text=f"🎓 Welcome, {fullname}", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Button(self.root, text="View Profile", width=30, command=self.view_profile).pack(pady=10)
        tk.Button(self.root, text="View Grades", width=30, command=self.view_grades).pack(pady=10)
        tk.Button(self.root, text="View ECA Activities", width=30, command=self.view_eca).pack(pady=10)
        tk.Button(self.root, text="Update Profile", width=30, command=self.update_profile).pack(pady=10)
        tk.Button(self.root, text="Logout", width=30, command=self.root.destroy, fg="red").pack(pady=20)

        self.root.mainloop()

    def view_profile(self):
        profile = f"👤 Name: {self.fullname}\n🆔 Username: {self.username}\n🎓 Role: Student"
        messagebox.showinfo("Your Profile", profile)

    def view_grades(self):
        try:
            with open("grades.txt", "r") as f:
                for line in f:
                    u, data = line.strip().split(":")
                    if u == self.username:
                        grades = data.split(",")
                        info = "📘 Your Grades:\n"
                        for i, g in enumerate(grades, 1):
                            info += f"  Subject {i}: {g}\n"
                        messagebox.showinfo("Grades", info)
                        return
            messagebox.showinfo("Grades", "No grades found.")
        except FileNotFoundError:
            messagebox.showerror("Error", "grades.txt not found.")

    def view_eca(self):
        try:
            with open("eca.txt", "r") as f:
                for line in f:
                    u, data = line.strip().split(":")
                    if u == self.username:
                        activities = data.split(",") if data.strip() else []
                        info = "🎯 Your ECA Activities:\n"
                        if activities:
                            for a in activities:
                                info += f"  - {a}\n"
                        else:
                            info += "  None"
                        messagebox.showinfo("ECA Activities", info)
                        return
            messagebox.showinfo("ECA Activities", "No ECA data found.")
        except FileNotFoundError:
            messagebox.showerror("Error", "eca.txt not found.")

    def update_profile(self):
        messagebox.showinfo("Coming Soon", "Profile update feature is under development.")
