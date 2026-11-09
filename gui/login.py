# import tkinter as tk
# from tkinter import messagebox

# from backend.authentication import login_user


# def show_login(root):

#     for widget in root.winfo_children():
#         widget.destroy()

#     root.configure(bg="#F2F4F8")

#     frame = tk.Frame(root, bg="#F2F4F8")
#     frame.pack(expand=True)

#     tk.Label(
#         frame,
#         text="USER LOGIN",
#         font=("Arial", 22, "bold"),
#         bg="#F2F4F8",
#         fg="#243B55"
#     ).pack(pady=20)

#     tk.Label(
#         frame,
#         text="User ID",
#         font=("Arial", 12),
#         bg="#F2F4F8"
#     ).pack()

#     user_id_entry = tk.Entry(
#         frame,
#         font=("Arial", 12),
#         width=30
#     )
#     user_id_entry.pack(pady=8)

#     tk.Label(
#         frame,
#         text="Password",
#         font=("Arial", 12),
#         bg="#F2F4F8"
#     ).pack()

#     password_entry = tk.Entry(
#         frame,
#         font=("Arial", 12),
#         width=30,
#         show="*"
#     )
#     password_entry.pack(pady=8)

#     def login():

#         user_id = user_id_entry.get().strip()
#         password = password_entry.get()

#         if not user_id or not password:

#             messagebox.showwarning(
#                 "Missing Details",
#                 "Please enter both User ID and Password."
#             )
#             return

#         user = login_user(user_id, password)

#         if user is None:

#             messagebox.showerror(
#                 "Login Failed",
#                 "Invalid User ID or Password."
#             )

#         elif user["role"] in ("STUDENT", "TEACHER"):

#             from gui.member import show_member
#             show_member(root, user)

#         elif user["role"] == "LIBRARIAN":

#             from gui.librarian import show_librarian
#             show_librarian(root, user)

#         else:

#             messagebox.showerror(
#                 "Error",
#                 "Invalid user role."
#             )

#     tk.Button(
#         frame,
#         text="Login",
#         font=("Arial", 12, "bold"),
#         width=20,
#         bg="#243B55",
#         fg="white",
#         command=login
#     ).pack(pady=15)

#     def go_home():

#         from gui.home import show_home
#         show_home(root)

#     tk.Button(
#         frame,
#         text="Back to Home",
#         font=("Arial", 11),
#         command=go_home
#     ).pack(pady=5)

import tkinter as tk
from tkinter import ttk, messagebox

from backend.authentication import login_user


def show_login(root):

    for widget in root.winfo_children():
        widget.destroy()

    frame = ttk.Frame(root, padding=40)
    frame.pack(expand=True)

    ttk.Label(
        frame,
        text="USER LOGIN",
        font=("Arial", 23, "bold")
    ).pack(pady=20)

    ttk.Label(
        frame,
        text="User ID"
    ).pack(anchor="w")

    user_id_entry = ttk.Entry(
        frame,
        width=35
    )
    user_id_entry.pack(pady=8)

    ttk.Label(
        frame,
        text="Password"
    ).pack(anchor="w")

    password_entry = ttk.Entry(
        frame,
        width=35,
        show="*"
    )
    password_entry.pack(pady=8)

    def login():

        user_id = user_id_entry.get().strip()
        password = password_entry.get()

        if not user_id or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter User ID and Password."
            )
            return

        user = login_user(user_id, password)

        if user is None:
            messagebox.showerror(
                "Login Failed",
                "Invalid User ID or Password."
            )
            return

        # Use uppercase Role because that is what
        # the corrected authentication.py returns.

        if user["Role"] == "LIBRARIAN":

            from gui.librarian import show_librarian
            show_librarian(root, user)

        elif user["Role"] in ("STUDENT", "TEACHER"):

            from gui.member import show_member
            show_member(root, user)

        else:
            messagebox.showerror(
                "Login Error",
                "Unknown user role."
            )

    def go_home():

        from gui.home import show_home
        show_home(root)

    ttk.Button(
        frame,
        text="Login",
        command=login,
        width=25
    ).pack(pady=15)

    ttk.Button(
        frame,
        text="Back",
        command=go_home,
        width=25
    ).pack(pady=5)