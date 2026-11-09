# import tkinter as tk
# from tkinter import ttk, messagebox

# from backend.book_operations import get_all_books

# from backend.issue_operations import (
#     request_book,
#     get_member_requests,
#     get_member_issues
# )

# from backend.fine_operations import (
#     get_member_fines,
#     get_outstanding_balance
# )


# def show_member(root, user):

#     for widget in root.winfo_children():
#         widget.destroy()

#     root.configure(bg="#F2F4F8")

#     header = tk.Frame(root, bg="#243B55")
#     header.pack(fill="x")

#     tk.Label(
#         header,
#         text="Welcome, " + user["First_Name"] + " " + user["Last_Name"],
#         font=("Arial", 16, "bold"),
#         bg="#243B55",
#         fg="white"
#     ).pack(side="left", padx=18, pady=12)

#     tk.Label(
#         header,
#         text=user["Role"],
#         bg="#243B55",
#         fg="white"
#     ).pack(side="right", padx=18)

#     notebook = ttk.Notebook(root)
#     notebook.pack(fill="both", expand=True, padx=10, pady=10)

#     def make_table(tab, columns):

#         table = ttk.Treeview(
#             tab,
#             columns=columns,
#             show="headings"
#         )

#         for col in columns:

#             table.heading(
#                 col,
#                 text=col.replace("_", " ").title()
#             )

#             table.column(col, width=140)

#         table.pack(
#             fill="both",
#             expand=True,
#             padx=8,
#             pady=8
#         )

#         return table

#     # ======================================
#     # BROWSE BOOKS
#     # ======================================

#     books_tab = tk.Frame(notebook)
#     notebook.add(books_tab, text="Browse Books")

#     book_table = make_table(
#         books_tab,
#         (
#             "book_id",
#             "book_name",
#             "author",
#             "category",
#             "available_copies"
#         )
#     )

#     # ======================================
#     # MY REQUESTS
#     # ======================================

#     requests_tab = tk.Frame(notebook)
#     notebook.add(requests_tab, text="My Requests")

#     request_table = make_table(
#         requests_tab,
#         (
#             "request_id",
#             "book_name",
#             "request_date",
#             "status",
#             "remarks"
#         )
#     )

#     # ======================================
#     # MY ISSUED BOOKS
#     # ======================================

#     issues_tab = tk.Frame(notebook)
#     notebook.add(issues_tab, text="My Issued Books")

#     issue_table = make_table(
#         issues_tab,
#         (
#             "issue_id",
#             "book_name",
#             "issue_date",
#             "due_date",
#             "return_date",
#             "status"
#         )
#     )

#     # ======================================
#     # MY FINES
#     # ======================================

#     fines_tab = tk.Frame(notebook)
#     notebook.add(fines_tab, text="My Fines")

#     balance_label = tk.Label(
#         fines_tab,
#         font=("Arial", 14, "bold")
#     )

#     balance_label.pack(pady=8)

#     fine_table = make_table(
#         fines_tab,
#         (
#             "fine_id",
#             "book_name",
#             "fine_type",
#             "fine_amount",
#             "payment_status",
#             "fine_date"
#         )
#     )

#     # ======================================
#     # TABLE REFRESH FUNCTION
#     # ======================================

#     def refill(table, rows):

#         for item in table.get_children():
#             table.delete(item)

#         for row in rows:
#             table.insert("", "end", values=row)

#     # ======================================
#     # LOAD BOOKS
#     # ======================================

#     def load_books():

#         books = get_all_books()

#         rows = [
#     (
#         book["Book_ID"],
#         book["Title"],
#         book["Author"],
#         book["Category"] or "",
#         book["Available_Copies"]
#     )
#     for book in books
# ]

#         refill(book_table, rows)

#     # ======================================
#     # LOAD REQUESTS
#     # ======================================

#     def load_requests():

#         requests = get_member_requests(user["User_ID"])

#         rows = [
#             (
#                 request["request_id"],
#                 request["book_name"],
#                 request["request_date"],
#                 request["status"],
#                 request["remarks"] or ""
#             )
#             for request in requests
#         ]

#         refill(request_table, rows)

#     # ======================================
#     # LOAD ISSUED BOOKS
#     # ======================================

#     def load_issues():

#         issues = get_member_issues(user["User_ID"])

#         rows = [
#             (
#                 issue["issue_id"],
#                 issue["book_name"],
#                 issue["issue_date"],
#                 issue["due_date"],
#                 issue["return_date"] or "-",
#                 issue["status"]
#             )
#             for issue in issues
#         ]

#         refill(issue_table, rows)

#     # ======================================
#     # LOAD FINES
#     # ======================================

#     def load_fines():

#         fines = get_member_fines(user["User_ID"])

#         rows = [
#             (
#                 fine["fine_id"],
#                 fine["book_name"],
#                 fine["fine_type"],
#                 fine["fine_amount"],
#                 fine["payment_status"],
#                 fine["fine_date"]
#             )
#             for fine in fines
#         ]

#         refill(fine_table, rows)

#         balance = get_outstanding_balance(user["User_ID"])

#         balance_label.config(
#             text="Outstanding Balance: Rs. " + str(balance)
#         )

#     # ======================================
#     # REQUEST SELECTED BOOK
#     # ======================================

#     def request_selected():

#         selected = book_table.selection()

#         if not selected:

#             messagebox.showwarning(
#                 "Select Book",
#                 "Please select a book first."
#             )

#             return

#         book_id = book_table.item(
#             selected[0],
#             "values"
#         )[0]

#         success, message = request_book(
#             user["User_ID"],
#             book_id
#         )

#         if success:
#             messagebox.showinfo("Book Request", message)
#         else:
#             messagebox.showerror("Book Request", message)

#         load_books()
#         load_requests()

#     tk.Button(
#         books_tab,
#         text="Request Selected Book",
#         command=request_selected,
#         bg="#287A68",
#         fg="white"
#     ).pack(pady=6)

#     # ======================================
#     # REFRESH ALL
#     # ======================================

#     def refresh_all():

#         load_books()
#         load_requests()
#         load_issues()
#         load_fines()

#     # ======================================
#     # LOGOUT
#     # ======================================

#     def logout():

#         from gui.home import show_home
#         show_home(root)

#     tk.Button(
#         root,
#         text="Refresh All",
#         command=refresh_all
#     ).pack(side="left", padx=12, pady=6)

#     tk.Button(
#         root,
#         text="Logout",
#         command=logout
#     ).pack(side="right", padx=12, pady=6)

#     refresh_all()










import tkinter as tk
from tkinter import ttk, messagebox

from backend.book_operations import get_all_books

from backend.issue_operations import (
    request_book,
    get_member_requests,
    get_member_issues
)

from backend.fine_operations import (
    get_member_fines,
    get_outstanding_balance
)


def show_member(root, user):

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#F2F4F8")

    user_id = user["User_ID"]

    header = tk.Frame(root, bg="#243B55")
    header.pack(fill="x")

    tk.Label(
        header,
        text="Welcome, " + user["First_Name"] + " " + user["Last_Name"],
        font=("Arial", 16, "bold"),
        bg="#243B55",
        fg="white"
    ).pack(side="left", padx=18, pady=12)

    tk.Label(
        header,
        text=user["Role"],
        bg="#243B55",
        fg="white"
    ).pack(side="right", padx=18)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    def make_table(tab, columns):

        table = ttk.Treeview(
            tab,
            columns=columns,
            show="headings"
        )

        for col in columns:
            table.heading(
                col,
                text=col.replace("_", " ").title()
            )
            table.column(col, width=140)

        table.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        return table

    # BROWSE BOOKS

    books_tab = tk.Frame(notebook)
    notebook.add(books_tab, text="Browse Books")

    book_table = make_table(
        books_tab,
        (
            "book_id",
            "book_name",
            "author",
            "category",
            "available_copies"
        )
    )

    # MY REQUESTS

    requests_tab = tk.Frame(notebook)
    notebook.add(requests_tab, text="My Requests")

    request_table = make_table(
        requests_tab,
        (
            "request_id",
            "book_name",
            "request_date",
            "status",
            "remarks"
        )
    )

    # MY ISSUED BOOKS

    issues_tab = tk.Frame(notebook)
    notebook.add(issues_tab, text="My Issued Books")

    issue_table = make_table(
        issues_tab,
        (
            "issue_id",
            "book_name",
            "issue_date",
            "due_date",
            "return_date",
            "status"
        )
    )

    # MY FINES

    fines_tab = tk.Frame(notebook)
    notebook.add(fines_tab, text="My Fines")

    balance_label = tk.Label(
        fines_tab,
        font=("Arial", 14, "bold")
    )
    balance_label.pack(pady=8)

    fine_table = make_table(
        fines_tab,
        (
            "fine_id",
            "book_name",
            "fine_type",
            "fine_amount",
            "payment_status",
            "fine_date"
        )
    )

    # TABLE REFRESH

    def refill(table, rows):

        for item in table.get_children():
            table.delete(item)

        for row in rows:
            table.insert("", "end", values=row)

    # LOAD BOOKS

    def load_books():

        books = get_all_books()

        rows = [
            (
                book["Book_ID"],
                book["Title"],
                book["Author"],
                book["Category"] or "",
                book["Available_Copies"]
            )
            for book in books
        ]

        refill(book_table, rows)

    # LOAD REQUESTS

    def load_requests():

        requests = get_member_requests(user_id)

        rows = [
            (
                request["Request_ID"],
                request["Title"],
                request["Request_Date"],
                request["Status"],
                request["Remarks"] or ""
            )
            for request in requests
        ]

        refill(request_table, rows)

    # LOAD ISSUED BOOKS

    def load_issues():

        issues = get_member_issues(user_id)

        rows = [
            (
                issue["Issue_ID"],
                issue["Title"],
                issue["Issue_Date"],
                issue["Due_Date"],
                issue["Return_Date"] or "-",
                issue["Status"]
            )
            for issue in issues
        ]

        refill(issue_table, rows)

    # LOAD FINES

    def load_fines():

        fines = get_member_fines(user_id)

        rows = [
            (
                fine["Fine_ID"],
                fine["Title"],
                fine["Fine_Type"],
                fine["Amount"],
                fine["Status"],
                fine["Fine_Date"]
            )
            for fine in fines
        ]

        refill(fine_table, rows)

        balance = get_outstanding_balance(user_id)

        balance_label.config(
            text="Outstanding Balance: Rs. " + str(balance)
        )

    # REQUEST SELECTED BOOK

    def request_selected():

        selected = book_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Book",
                "Please select a book first."
            )
            return

        book_id = book_table.item(
            selected[0],
            "values"
        )[0]

        success, message = request_book(
            user_id,
            book_id
        )

        if success:
            messagebox.showinfo("Book Request", message)
        else:
            messagebox.showerror("Book Request", message)

        load_books()
        load_requests()

    tk.Button(
        books_tab,
        text="Request Selected Book",
        command=request_selected,
        bg="#287A68",
        fg="white"
    ).pack(pady=6)

    # REFRESH ALL

    def refresh_all():

        load_books()
        load_requests()
        load_issues()
        load_fines()

    # LOGOUT

    def logout():

        from gui.home import show_home
        show_home(root)

    tk.Button(
        root,
        text="Refresh All",
        command=refresh_all
    ).pack(side="left", padx=12, pady=6)

    tk.Button(
        root,
        text="Logout",
        command=logout
    ).pack(side="right", padx=12, pady=6)

    refresh_all()
