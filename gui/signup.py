import tkinter as tk
from tkinter import messagebox

from backend.authentication import register_user


def show_signup(root):

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#F2F4F8")

    frame = tk.Frame(root, bg="#F2F4F8")
    frame.pack(expand=True)

    tk.Label(
        frame,
        text="NEW USER REGISTRATION",
        font=("Arial", 20, "bold"),
        bg="#F2F4F8",
        fg="#243B55"
    ).pack(pady=12)

    fields = {}

    field_names = [
        "User ID",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Password"
    ]

    for field in field_names:

        tk.Label(
            frame,
            text=field,
            bg="#F2F4F8"
        ).pack()

        entry = tk.Entry(
            frame,
            width=30,
            show="*" if field == "Password" else ""
        )

        entry.pack(pady=3)

        fields[field] = entry

    tk.Label(
        frame,
        text="Select Role",
        bg="#F2F4F8"
    ).pack(pady=(7, 0))

    role = tk.StringVar(value="STUDENT")

    tk.OptionMenu(
        frame,
        role,
        "STUDENT",
        "TEACHER"
    ).pack()

    def register():

        values = {
            key: entry.get().strip()
            for key, entry in fields.items()
        }

        required_fields = [
            "User ID",
            "First Name",
            "Last Name",
            "Email",
            "Password"
        ]

        if not all(values[field] for field in required_fields):

            messagebox.showwarning(
                "Missing Details",
                "Please fill in all required fields."
            )
            return

        if len(values["Password"]) < 6:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 6 characters."
            )
            return

        success, message = register_user(
            values["User ID"],
            values["First Name"],
            values["Last Name"],
            values["Email"],
            values["Phone"],
            values["Password"],
            role.get()
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            from gui.login import show_login
            show_login(root)

        else:

            messagebox.showerror(
                "Registration Failed",
                message
            )

    tk.Button(
        frame,
        text="Register",
        width=20,
        bg="#287A68",
        fg="white",
        command=register
    ).pack(pady=10)

    def go_home():

        from gui.home import show_home
        show_home(root)

    tk.Button(
        frame,
        text="Back to Home",
        command=go_home
    ).pack(pady=4)