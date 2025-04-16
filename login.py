from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from user import Admin, Student
from AdminDashboard import AdminDashboard  
from StudentDashboard import StudentDashboard  

class login_system:
    def __init__(self, root):
        self.root = root
        self.root.title("login system")
        self.root.geometry("1100x600")
        self.root.config(bg="white")

        # === static image ========
        image = Image.open("ok.png")
        self.photo = ImageTk.PhotoImage(image)
        img_label = Label(self.root, image=self.photo, bg="white")
        img_label.place(x=10, y=100)

        # === Login frame ===
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=600, y=90, width=350, height=350)

        title1 = Label(login_frame, text="Welcome", font=("Elephant", 30, "bold"), bg="white")
        title1.place(x=0, y=30, relwidth=1)

        title2 = Label(login_frame, text="Login to your account to continue", font=("times new roman", 12), bg="white", fg="#767171")
        title2.place(x=0, y=75, relwidth=1)

        #==username and passsword lbl====
        lbl_user = Label(login_frame, text="Username", font=("times new roman", 15, "bold"), bg="white", fg="#767171")
        lbl_user.place(x=50, y=100)
        self.txt_username = Entry(login_frame, font=("times new roman", 15, "bold"), bg="lightgray")
        self.txt_username.place(x=50, y=140, width=250)

        lbl_pass = Label(login_frame, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="#767171")
        lbl_pass.place(x=50, y=170)
        self.txt_password = Entry(login_frame, font=("times new roman", 15, "bold"), bg="lightgray", show="*")
        self.txt_password.place(x=50, y=205, width=250)

        #==login button lbl===
        btn_login = Button(login_frame, text="Log in", font=("arial rounded mt bold", 15), bg="black", activebackground="white", fg="white", command=self.login)
        btn_login.place(x=75, y=300, width=200, height=35)

        hr = Label(login_frame, bg="lightgray")
        hr.place(x=50, y=250, width=250, height=2)

        # === Animation images ===
        self.im1 = ImageTk.PhotoImage(Image.open("ok3.webp").resize((369, 220)))
        self.im2 = ImageTk.PhotoImage(Image.open("ok2.webp").resize((369, 220)))
        self.image = self.im1  # Set initial image

        self.lbl_change_Image = Label(self.root, bg="white")
        self.lbl_change_Image.place(x=146, y=134, width=369, height=220)

        # Start animation
        self.animate()

    def animate(self):
        self.image = self.im2 if self.image == self.im1 else self.im1
        self.lbl_change_Image.configure(image=self.image)
        self.lbl_change_Image.image = self.image
        self.root.after(2000, self.animate)

    def load_users(self):
        users = {}
        try:
            with open("users.txt", "r") as f:
                for line in f:
                    username, fullname, role = line.strip().split(",")
                    users[username] = {"fullname": fullname, "role": role}
        except FileNotFoundError:
            messagebox.showerror("Error", "users.txt not found!", parent=self.root)
        return users

    def load_passwords(self):
        passwords = {}
        try:
            with open("passwords.txt", "r") as f:
                for line in f:
                    username, password = line.strip().split(",")
                    passwords[username] = password
        except FileNotFoundError:
            messagebox.showerror("Error", "passwords.txt not found!", parent=self.root)
        return passwords

    def login(self):
        username = self.txt_username.get().strip()
        password = self.txt_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        users = self.load_users()
        passwords = self.load_passwords()

        if username in passwords and passwords[username] == password:
            fullname = users[username]["fullname"]
            role = users[username]["role"]
            messagebox.showinfo("Success", f"✅ Welcome {fullname}!", parent=self.root)
            self.redirect_user(username, fullname, role)
        else:
            messagebox.showerror("Error", "Invalid username or password!", parent=self.root)

    def redirect_user(self, username, fullname, role):
        self.root.destroy()
        if role == "admin":
        # Open Admin Dashboard menu, not directly analytics
            admin_dashboard = AdminDashboard(username, fullname)
            
        elif role == "student":
        # Open Student Dashboard menu, not directly analytics
            student_dashboard = StudentDashboard(username, fullname)
            


# Run app
root = Tk()
obj = login_system(root)
root.mainloop()
