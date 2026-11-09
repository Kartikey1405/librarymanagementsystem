# from datetime import date, timedelta

# from database.connection import connect_database


# def request_book(user_id, book_id):

#     connection = connect_database()

#     if connection is None:
#         return False, "Database connection failed."

#     cursor = connection.cursor()

#     try:
#         cursor.execute("""
#             SELECT Available_Copies
#             FROM Books
#             WHERE Book_ID = %s
#         """, (book_id,))

#         book = cursor.fetchone()

#         if book is None:
#             return False, "Book not found."

#         if book[0] <= 0:
#             return False, "No copies are currently available."

#         cursor.execute("""
#             SELECT Request_ID
#             FROM Issue_Requests
#             WHERE User_ID = %s
#             AND Book_ID = %s
#             AND Status = 'PENDING'
#         """, (user_id, book_id))

#         if cursor.fetchone():
#             return False, "You already have a pending request for this book."

#         cursor.execute("""
#             INSERT INTO Issue_Requests
#             (User_ID, Book_ID, Request_Date, Status)
#             VALUES (%s, %s, %s, 'PENDING')
#         """, (user_id, book_id, date.today()))

#         connection.commit()
#         return True, "Book request submitted."

#     except Exception as error:
#         connection.rollback()
#         return False, str(error)

#     finally:
#         cursor.close()
#         connection.close()


# def get_member_requests(user_id):

#     connection = connect_database()

#     if connection is None:
#         return []

#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT R.Request_ID, R.Book_ID, B.Title,
#                    R.Request_Date, R.Status
#             FROM Issue_Requests R
#             JOIN Books B ON R.Book_ID = B.Book_ID
#             WHERE R.User_ID = %s
#             ORDER BY R.Request_ID DESC
#         """, (user_id,))

#         return cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()


# def get_pending_requests():

#     connection = connect_database()

#     if connection is None:
#         return []

#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT R.Request_ID, R.User_ID,
#                    U.First_Name, U.Last_Name,
#                    R.Book_ID, B.Title, R.Request_Date
#             FROM Issue_Requests R
#             JOIN Users U ON R.User_ID = U.User_ID
#             JOIN Books B ON R.Book_ID = B.Book_ID
#             WHERE R.Status = 'PENDING'
#             ORDER BY R.Request_Date
#         """)

#         return cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()


# def approve_request(request_id, loan_days):

#     if loan_days not in (7, 15):
#         return False, "Loan period must be 7 or 15 days."

#     connection = connect_database()

#     if connection is None:
#         return False, "Database connection failed."

#     cursor = connection.cursor(dictionary=True)

#     try:
#         connection.start_transaction()

#         cursor.execute("""
#             SELECT User_ID, Book_ID, Status
#             FROM Issue_Requests
#             WHERE Request_ID = %s
#             FOR UPDATE
#         """, (request_id,))

#         request = cursor.fetchone()

#         if request is None or request["Status"] != "PENDING":
#             connection.rollback()
#             return False, "Request is no longer pending."

#         cursor.execute("""
#             SELECT Available_Copies
#             FROM Books
#             WHERE Book_ID = %s
#             FOR UPDATE
#         """, (request["Book_ID"],))

#         book = cursor.fetchone()

#         if book is None or book["Available_Copies"] <= 0:
#             connection.rollback()
#             return False, "No copies are available."

#         issue_date = date.today()
#         due_date = issue_date + timedelta(days=loan_days)

#         cursor.execute("""
#             INSERT INTO Issue_Records
#             (User_ID, Book_ID, Issue_Date, Due_Date, Status)
#             VALUES (%s, %s, %s, %s, 'ISSUED')
#         """, (
#             request["User_ID"],
#             request["Book_ID"],
#             issue_date,
#             due_date
#         ))

#         cursor.execute("""
#             UPDATE Books
#             SET Available_Copies = Available_Copies - 1
#             WHERE Book_ID = %s
#         """, (request["Book_ID"],))

#         cursor.execute("""
#             UPDATE Issue_Requests
#             SET Status = 'ISSUED'
#             WHERE Request_ID = %s
#         """, (request_id,))

#         connection.commit()
#         return True, "Book issued successfully."

#     except Exception as error:
#         connection.rollback()
#         return False, str(error)

#     finally:
#         cursor.close()
#         connection.close()


# def reject_request(request_id):

#     connection = connect_database()

#     if connection is None:
#         return False

#     cursor = connection.cursor()

#     try:
#         cursor.execute("""
#             UPDATE Issue_Requests
#             SET Status = 'REJECTED'
#             WHERE Request_ID = %s
#             AND Status = 'PENDING'
#         """, (request_id,))

#         connection.commit()
#         return cursor.rowcount > 0

#     except Exception as error:
#         connection.rollback()
#         print(error)
#         return False

#     finally:
#         cursor.close()
#         connection.close()


# def get_member_issues(user_id):

#     connection = connect_database()

#     if connection is None:
#         return []

#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT I.Issue_ID, I.Book_ID, B.Title,
#                    I.Issue_Date, I.Due_Date,
#                    I.Return_Date, I.Status
#             FROM Issue_Records I
#             JOIN Books B ON I.Book_ID = B.Book_ID
#             WHERE I.User_ID = %s
#             ORDER BY I.Issue_ID DESC
#         """, (user_id,))

#         return cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()


# def get_all_issues():

#     connection = connect_database()

#     if connection is None:
#         return []

#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT I.Issue_ID, I.User_ID,
#                    U.First_Name, U.Last_Name,
#                    I.Book_ID, B.Title,
#                    I.Issue_Date, I.Due_Date,
#                    I.Return_Date, I.Status
#             FROM Issue_Records I
#             JOIN Users U ON I.User_ID = U.User_ID
#             JOIN Books B ON I.Book_ID = B.Book_ID
#             ORDER BY I.Issue_ID DESC
#         """)

#         return cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()


# def return_book(issue_id, damage_amount=0):

#     if damage_amount < 0:
#         return False, "Damage amount cannot be negative."

#     connection = connect_database()

#     if connection is None:
#         return False, "Database connection failed."

#     cursor = connection.cursor(dictionary=True)

#     try:
#         connection.start_transaction()

#         cursor.execute("""
#             SELECT Book_ID, Due_Date, Status
#             FROM Issue_Records
#             WHERE Issue_ID = %s
#             FOR UPDATE
#         """, (issue_id,))

#         issue = cursor.fetchone()

#         if issue is None or issue["Status"] != "ISSUED":
#             connection.rollback()
#             return False, "This book is already returned or record not found."

#         return_date = date.today()
#         overdue_days = max(0, (return_date - issue["Due_Date"]).days)
#         late_fine = overdue_days * 1

#         cursor.execute("""
#             UPDATE Issue_Records
#             SET Return_Date = %s,
#                 Status = 'RETURNED'
#             WHERE Issue_ID = %s
#         """, (return_date, issue_id))

#         cursor.execute("""
#             UPDATE Books
#             SET Available_Copies = Available_Copies + 1
#             WHERE Book_ID = %s
#         """, (issue["Book_ID"],))

#         if late_fine > 0:
#             cursor.execute("""
#                 INSERT INTO Fines
#                 (Issue_ID, Fine_Type, Amount, Status)
#                 VALUES (%s, 'LATE', %s, 'UNPAID')
#             """, (issue_id, late_fine))

#         if damage_amount > 0:
#             cursor.execute("""
#                 INSERT INTO Fines
#                 (Issue_ID, Fine_Type, Amount, Status)
#                 VALUES (%s, 'DAMAGE', %s, 'UNPAID')
#             """, (issue_id, damage_amount))

#         connection.commit()

#         return True, (
#             "Book returned successfully. "
#             f"Late fine: Rs. {late_fine}. "
#             f"Damage fine: Rs. {damage_amount}."
#         )

#     except Exception as error:
#         connection.rollback()
#         return False, str(error)

#     finally:
#         cursor.close()
#         connection.close()


from datetime import date, timedelta

from database.connection import connect_database


def request_book(user_id, book_id):

    connection = connect_database()

    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT available_copies
            FROM Books
            WHERE book_id = %s
        """, (book_id,))

        book = cursor.fetchone()

        if book is None:
            return False, "Book not found."

        if book[0] <= 0:
            return False, "No copies are currently available."

        cursor.execute("""
            SELECT request_id
            FROM Issue_Requests
            WHERE user_id = %s
              AND book_id = %s
              AND status = 'PENDING'
        """, (user_id, book_id))

        if cursor.fetchone():
            return False, "You already have a pending request."

        cursor.execute("""
            INSERT INTO Issue_Requests
            (user_id, book_id, request_date, status)
            VALUES (%s, %s, %s, 'PENDING')
        """, (user_id, book_id, date.today()))

        connection.commit()
        return True, "Book request submitted successfully."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        cursor.close()
        connection.close()


def get_member_requests(user_id):

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                R.request_id AS Request_ID,
                R.book_id AS Book_ID,
                B.book_name AS Title,
                R.request_date AS Request_Date,
                R.status AS Status,
                R.remarks AS Remarks
            FROM Issue_Requests R
            JOIN Books B ON R.book_id = B.book_id
            WHERE R.user_id = %s
            ORDER BY R.request_id DESC
        """, (user_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_pending_requests():

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                R.request_id AS Request_ID,
                R.user_id AS User_ID,
                U.first_name AS First_Name,
                U.last_name AS Last_Name,
                R.book_id AS Book_ID,
                B.book_name AS Title,
                R.request_date AS Request_Date
            FROM Issue_Requests R
            JOIN Users U ON R.user_id = U.user_id
            JOIN Books B ON R.book_id = B.book_id
            WHERE R.status = 'PENDING'
            ORDER BY R.request_date
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def approve_request(request_id, loan_days):

    if loan_days not in (7, 15):
        return False, "Loan period must be 7 or 15 days."

    connection = connect_database()

    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor(dictionary=True)

    try:
        connection.start_transaction()

        cursor.execute("""
            SELECT user_id, book_id, status
            FROM Issue_Requests
            WHERE request_id = %s
            FOR UPDATE
        """, (request_id,))

        request = cursor.fetchone()

        if request is None or request["status"] != "PENDING":
            connection.rollback()
            return False, "Request is no longer pending."

        cursor.execute("""
            SELECT available_copies
            FROM Books
            WHERE book_id = %s
            FOR UPDATE
        """, (request["book_id"],))

        book = cursor.fetchone()

        if book is None or book["available_copies"] <= 0:
            connection.rollback()
            return False, "No copies are currently available."

        issue_date = date.today()
        due_date = issue_date + timedelta(days=loan_days)

        cursor.execute("""
            INSERT INTO Issue_Records
            (request_id, user_id, book_id, issue_date,
             loan_days, due_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'ISSUED')
        """, (
            request_id,
            request["user_id"],
            request["book_id"],
            issue_date,
            loan_days,
            due_date
        ))

        cursor.execute("""
            UPDATE Books
            SET available_copies = available_copies - 1
            WHERE book_id = %s
        """, (request["book_id"],))

        cursor.execute("""
            UPDATE Issue_Requests
            SET status = 'APPROVED'
            WHERE request_id = %s
        """, (request_id,))

        connection.commit()
        return True, "Book issued successfully."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        cursor.close()
        connection.close()


def reject_request(request_id):

    connection = connect_database()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE Issue_Requests
            SET status = 'REJECTED'
            WHERE request_id = %s
              AND status = 'PENDING'
        """, (request_id,))

        connection.commit()
        return cursor.rowcount > 0

    except Exception as error:
        connection.rollback()
        print(error)
        return False

    finally:
        cursor.close()
        connection.close()


def get_member_issues(user_id):

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                I.issue_id AS Issue_ID,
                I.book_id AS Book_ID,
                B.book_name AS Title,
                I.issue_date AS Issue_Date,
                I.due_date AS Due_Date,
                I.return_date AS Return_Date,
                I.status AS Status,
                I.return_condition AS Return_Condition
            FROM Issue_Records I
            JOIN Books B ON I.book_id = B.book_id
            WHERE I.user_id = %s
            ORDER BY I.issue_id DESC
        """, (user_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_all_issues():

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                I.issue_id AS Issue_ID,
                I.user_id AS User_ID,
                U.first_name AS First_Name,
                U.last_name AS Last_Name,
                I.book_id AS Book_ID,
                B.book_name AS Title,
                I.issue_date AS Issue_Date,
                I.due_date AS Due_Date,
                I.return_date AS Return_Date,
                I.status AS Status
            FROM Issue_Records I
            JOIN Users U ON I.user_id = U.user_id
            JOIN Books B ON I.book_id = B.book_id
            ORDER BY I.issue_id DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def return_book(issue_id, damage_amount=0):

    if damage_amount < 0:
        return False, "Damage amount cannot be negative."

    connection = connect_database()

    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor(dictionary=True)

    try:
        connection.start_transaction()

        cursor.execute("""
            SELECT book_id, due_date, status
            FROM Issue_Records
            WHERE issue_id = %s
            FOR UPDATE
        """, (issue_id,))

        issue = cursor.fetchone()

        if issue is None or issue["status"] != "ISSUED":
            connection.rollback()
            return False, "Issue record not found or already returned."

        return_date = date.today()
        overdue_days = max(0, (return_date - issue["due_date"]).days)
        late_fine = overdue_days * 1

        return_condition = "DAMAGED" if damage_amount > 0 else "GOOD"

        cursor.execute("""
            UPDATE Issue_Records
            SET return_date = %s,
                status = 'RETURNED',
                return_condition = %s
            WHERE issue_id = %s
        """, (return_date, return_condition, issue_id))

        cursor.execute("""
            UPDATE Books
            SET available_copies = available_copies + 1
            WHERE book_id = %s
        """, (issue["book_id"],))

        if late_fine > 0:
            cursor.execute("""
                INSERT INTO Fines
                (issue_id, fine_type, fine_amount,
                 fine_date, payment_status, remarks)
                VALUES (%s, 'LATE', %s, %s, 'PENDING', %s)
            """, (
                issue_id,
                late_fine,
                return_date,
                f"{overdue_days} overdue days"
            ))

        if damage_amount > 0:
            cursor.execute("""
                INSERT INTO Fines
                (issue_id, fine_type, fine_amount,
                 fine_date, payment_status, remarks)
                VALUES (%s, 'DAMAGE', %s, %s, 'PENDING', %s)
            """, (
                issue_id,
                damage_amount,
                return_date,
                "Damage fine entered by librarian"
            ))

        connection.commit()

        return True, (
            f"Book returned successfully. "
            f"Late fine: Rs. {late_fine}. "
            f"Damage fine: Rs. {damage_amount}."
        )

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        cursor.close()
        connection.close()