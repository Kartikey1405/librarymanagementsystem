import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from backend.book_operations import (
    add_book,
    get_all_books,
    delete_book
)

from backend.member_operations import get_all_members

from backend.issue_operations import (
    get_pending_requests,
    approve_request,
    reject_request,
    get_all_issues,
    return_book
)

from backend.fine_operations import (
    get_all_fines,
    mark_fine_paid
)


def show_librarian(root, user):

    for widget in root.winfo_children():
        widget.destroy()

    main_frame = ttk.Frame(root, padding=15)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(
        main_frame,
        text="LIBRARIAN DASHBOARD",
        font=("Arial", 22, "bold")
    ).pack(pady=10)

    ttk.Label(
        main_frame,
        text=f"Welcome, {user['First_Name']} {user['Last_Name']}"
    ).pack(pady=5)

    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill="both", expand=True, pady=10)

    request_tab = ttk.Frame(notebook, padding=10)
    book_tab = ttk.Frame(notebook, padding=10)
    member_tab = ttk.Frame(notebook, padding=10)
    issue_tab = ttk.Frame(notebook, padding=10)
    fine_tab = ttk.Frame(notebook, padding=10)

    notebook.add(request_tab, text="Issue Requests")
    notebook.add(book_tab, text="Book Management")
    notebook.add(member_tab, text="Members")
    notebook.add(issue_tab, text="Issue Records")
    notebook.add(fine_tab, text="Fine Management")

    # =====================================
    # 1. ISSUE REQUESTS
    # =====================================

    request_columns = (
        "Request_ID",
        "User_ID",
        "Member_Name",
        "Book_ID",
        "Title",
        "Request_Date"
    )

    request_tree = ttk.Treeview(
        request_tab,
        columns=request_columns,
        show="headings",
        height=12
    )

    for column in request_columns:
        request_tree.heading(
            column,
            text=column.replace("_", " ")
        )
        request_tree.column(column, width=140)

    request_tree.pack(fill="both", expand=True)

    def refresh_requests():

        for item in request_tree.get_children():
            request_tree.delete(item)

        requests = get_pending_requests()

        for record in requests:
            request_tree.insert(
                "",
                "end",
                values=(
                    record["Request_ID"],
                    record["User_ID"],
                    record["First_Name"] + " " + record["Last_Name"],
                    record["Book_ID"],
                    record["Title"],
                    record["Request_Date"]
                )
            )

    def approve_selected():

        selected = request_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select a request."
            )
            return

        values = request_tree.item(
            selected[0],
            "values"
        )

        request_id = int(values[0])

        loan_days = simpledialog.askinteger(
            "Loan Period",
            "Enter loan period (7 or 15 days):",
            parent=root
        )

        if loan_days is None:
            return

        success, message = approve_request(
            request_id,
            loan_days
        )

        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

        refresh_requests()
        refresh_issues()
        refresh_books()

    def reject_selected():

        selected = request_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select a request."
            )
            return

        values = request_tree.item(
            selected[0],
            "values"
        )

        request_id = int(values[0])

        confirm = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to reject this request?"
        )

        if not confirm:
            return

        if reject_request(request_id):
            messagebox.showinfo(
                "Success",
                "Request rejected successfully."
            )
        else:
            messagebox.showerror(
                "Error",
                "Unable to reject request."
            )

        refresh_requests()

    request_buttons = ttk.Frame(request_tab)
    request_buttons.pack(pady=8)

    ttk.Button(
        request_buttons,
        text="Approve Request",
        command=approve_selected
    ).pack(side="left", padx=5)

    ttk.Button(
        request_buttons,
        text="Reject Request",
        command=reject_selected
    ).pack(side="left", padx=5)

    ttk.Button(
        request_buttons,
        text="Refresh",
        command=refresh_requests
    ).pack(side="left", padx=5)

    # =====================================
    # 2. BOOK MANAGEMENT
    # =====================================

    book_columns = (
        "Book_ID",
        "Title",
        "Author",
        "Category",
        "Publisher",
        "Total_Copies",
        "Available_Copies"
    )

    book_tree = ttk.Treeview(
        book_tab,
        columns=book_columns,
        show="headings",
        height=10
    )

    for column in book_columns:
        book_tree.heading(
            column,
            text=column.replace("_", " ")
        )
        book_tree.column(column, width=120)

    book_tree.pack(fill="both", expand=True)

    form_frame = ttk.LabelFrame(
        book_tab,
        text="Add New Book",
        padding=10
    )

    form_frame.pack(fill="x", pady=10)

    # Book ID is automatically generated by MySQL.
    # Therefore, it is not included in this form.

    book_fields = [
        "Book Name",
        "Author",
        "Category",
        "Publisher",
        "Total Copies"
    ]

    book_entries = {}

    for index, field in enumerate(book_fields):

        row = index // 3
        column = (index % 3) * 2

        ttk.Label(
            form_frame,
            text=field
        ).grid(
            row=row,
            column=column,
            padx=5,
            pady=5,
            sticky="w"
        )

        entry = ttk.Entry(
            form_frame,
            width=18
        )

        entry.grid(
            row=row,
            column=column + 1,
            padx=5,
            pady=5
        )

        book_entries[field] = entry

    def refresh_books():

        for item in book_tree.get_children():
            book_tree.delete(item)

        books = get_all_books()

        for book in books:
            book_tree.insert(
                "",
                "end",
                values=(
                    book["Book_ID"],
                    book["Title"],
                    book["Author"],
                    book["Category"],
                    book["Publisher"],
                    book["Total_Copies"],
                    book["Available_Copies"]
                )
            )

    def add_new_book():

        values = {
            field: book_entries[field].get().strip()
            for field in book_fields
        }

        if not all(values.values()):
            messagebox.showwarning(
                "Missing Information",
                "Please fill all book details."
            )
            return

        try:
            total_copies = int(values["Total Copies"])

            if total_copies <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Total Copies must be a positive whole number."
            )
            return

        success, message = add_book(
            values["Book Name"],
            values["Author"],
            values["Category"],
            values["Publisher"],
            total_copies
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            for entry in book_entries.values():
                entry.delete(0, tk.END)

            refresh_books()

        else:
            messagebox.showerror(
                "Error",
                message
            )

    def delete_selected_book():

        selected = book_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select a book."
            )
            return

        values = book_tree.item(
            selected[0],
            "values"
        )

        book_id = int(values[0])

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this book?"
        )

        if not confirm:
            return

        success, message = delete_book(book_id)

        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

        refresh_books()

    book_buttons = ttk.Frame(book_tab)
    book_buttons.pack(pady=8)

    ttk.Button(
        book_buttons,
        text="Add Book",
        command=add_new_book
    ).pack(side="left", padx=5)

    ttk.Button(
        book_buttons,
        text="Delete Selected Book",
        command=delete_selected_book
    ).pack(side="left", padx=5)

    ttk.Button(
        book_buttons,
        text="Refresh Books",
        command=refresh_books
    ).pack(side="left", padx=5)

    # =====================================
    # 3. MEMBER MANAGEMENT
    # =====================================

    member_columns = (
        "User_ID",
        "First_Name",
        "Last_Name",
        "Email",
        "Phone",
        "Role"
    )

    member_tree = ttk.Treeview(
        member_tab,
        columns=member_columns,
        show="headings",
        height=15
    )

    for column in member_columns:
        member_tree.heading(
            column,
            text=column.replace("_", " ")
        )
        member_tree.column(column, width=140)

    member_tree.pack(fill="both", expand=True)

    def refresh_members():

        for item in member_tree.get_children():
            member_tree.delete(item)

        members = get_all_members()

        for member in members:
            member_tree.insert(
                "",
                "end",
                values=(
                    member["User_ID"],
                    member["First_Name"],
                    member["Last_Name"],
                    member["Email"],
                    member["Phone"],
                    member["Role"]
                )
            )

    ttk.Button(
        member_tab,
        text="Refresh Members",
        command=refresh_members
    ).pack(pady=8)

    # =====================================
    # 4. ISSUE RECORDS
    # =====================================

    issue_columns = (
        "Issue_ID",
        "User_ID",
        "Member_Name",
        "Book_ID",
        "Title",
        "Issue_Date",
        "Due_Date",
        "Return_Date",
        "Status"
    )

    issue_tree = ttk.Treeview(
        issue_tab,
        columns=issue_columns,
        show="headings",
        height=13
    )

    for column in issue_columns:
        issue_tree.heading(
            column,
            text=column.replace("_", " ")
        )
        issue_tree.column(column, width=120)

    issue_tree.pack(fill="both", expand=True)

    def refresh_issues():

        for item in issue_tree.get_children():
            issue_tree.delete(item)

        issues = get_all_issues()

        for record in issues:
            issue_tree.insert(
                "",
                "end",
                values=(
                    record["Issue_ID"],
                    record["User_ID"],
                    record["First_Name"] + " " + record["Last_Name"],
                    record["Book_ID"],
                    record["Title"],
                    record["Issue_Date"],
                    record["Due_Date"],
                    record["Return_Date"] or "-",
                    record["Status"]
                )
            )

    def return_selected_book():

        selected = issue_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select an issue record."
            )
            return

        values = issue_tree.item(
            selected[0],
            "values"
        )

        if values[8] != "ISSUED":
            messagebox.showwarning(
                "Already Returned",
                "This book has already been returned."
            )
            return

        issue_id = int(values[0])

        damaged = messagebox.askyesno(
            "Book Condition",
            "Is the returned book damaged?"
        )

        damage_amount = 0

        if damaged:

            damage_amount = simpledialog.askfloat(
                "Damage Fine",
                "Enter damage fine amount (Rs.):",
                parent=root,
                minvalue=0.01
            )

            if damage_amount is None:
                return

        success, message = return_book(
            issue_id,
            damage_amount
        )

        if success:
            messagebox.showinfo(
                "Return Confirmed",
                message
            )
        else:
            messagebox.showerror(
                "Error",
                message
            )

        refresh_issues()
        refresh_books()
        refresh_fines()

    issue_buttons = ttk.Frame(issue_tab)
    issue_buttons.pack(pady=8)

    ttk.Button(
        issue_buttons,
        text="Confirm Return",
        command=return_selected_book
    ).pack(side="left", padx=5)

    ttk.Button(
        issue_buttons,
        text="Refresh Records",
        command=refresh_issues
    ).pack(side="left", padx=5)

    # =====================================
    # 5. FINE MANAGEMENT
    # =====================================

    fine_columns = (
        "Fine_ID",
        "Issue_ID",
        "User_ID",
        "Member_Name",
        "Title",
        "Fine_Type",
        "Amount",
        "Status"
    )

    fine_tree = ttk.Treeview(
        fine_tab,
        columns=fine_columns,
        show="headings",
        height=13
    )

    for column in fine_columns:
        fine_tree.heading(
            column,
            text=column.replace("_", " ")
        )
        fine_tree.column(column, width=120)

    fine_tree.pack(fill="both", expand=True)

    def refresh_fines():

        for item in fine_tree.get_children():
            fine_tree.delete(item)

        fines = get_all_fines()

        for fine in fines:
            fine_tree.insert(
                "",
                "end",
                values=(
                    fine["Fine_ID"],
                    fine["Issue_ID"],
                    fine["User_ID"],
                    fine["First_Name"] + " " + fine["Last_Name"],
                    fine["Title"],
                    fine["Fine_Type"],
                    fine["Amount"],
                    fine["Status"]
                )
            )

    def pay_selected_fine():

        selected = fine_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select a fine."
            )
            return

        values = fine_tree.item(
            selected[0],
            "values"
        )

        fine_id = int(values[0])

        if values[7] == "PAID":
            messagebox.showinfo(
                "Already Paid",
                "This fine has already been paid."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Payment",
            "Confirm that this fine has been paid?"
        )

        if not confirm:
            return

        if mark_fine_paid(fine_id):
            messagebox.showinfo(
                "Success",
                "Fine marked as paid."
            )
        else:
            messagebox.showerror(
                "Error",
                "Unable to update fine status."
            )

        refresh_fines()

    fine_buttons = ttk.Frame(fine_tab)
    fine_buttons.pack(pady=8)

    ttk.Button(
        fine_buttons,
        text="Mark Fine as Paid",
        command=pay_selected_fine
    ).pack(side="left", padx=5)

    ttk.Button(
        fine_buttons,
        text="Refresh Fines",
        command=refresh_fines
    ).pack(side="left", padx=5)

    # =====================================
    # LOGOUT
    # =====================================

    def logout():

        from gui.home import show_home
        show_home(root)

    ttk.Button(
        main_frame,
        text="Logout",
        command=logout
    ).pack(pady=8)

    # Initial data loading

    refresh_requests()
    refresh_books()
    refresh_members()
    refresh_issues()
    refresh_fines()