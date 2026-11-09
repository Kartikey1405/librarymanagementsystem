import tkinter as tk


def show_home(root):

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#F2F4F8")

    frame = tk.Frame(root, bg="#F2F4F8")
    frame.pack(expand=True)

    def open_login():
        from gui.login import show_login
        show_login(root)

    def open_signup():
        from gui.signup import show_signup
        show_signup(root)

    tk.Label(
        frame,
        text="LIBRARY MANAGEMENT SYSTEM",
        font=("Arial", 24, "bold"),
        bg="#F2F4F8",
        fg="#243B55"
    ).pack(pady=25)

    tk.Label(
        frame,
        text="Welcome to our Digital Library",
        font=("Arial", 14),
        bg="#F2F4F8",
        fg="#555555"
    ).pack(pady=10)

    tk.Button(
        frame,
        text="Login",
        font=("Arial", 13, "bold"),
        width=22,
        bg="#243B55",
        fg="white",
        command=open_login
    ).pack(pady=15)

    tk.Button(
        frame,
        text="New User? Sign Up",
        font=("Arial", 13, "bold"),
        width=22,
        bg="#287A68",
        fg="white",
        command=open_signup
    ).pack(pady=10)

    tk.Label(
        frame,
        text="Python + Tkinter + MySQL",
        font=("Arial", 10),
        bg="#F2F4F8",
        fg="#777777"
    ).pack(pady=30)