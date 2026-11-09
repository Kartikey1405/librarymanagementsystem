# from database.connection import connect_database


# def get_member_fines(user_id):

#     connection = connect_database()

#     if connection is None:
#         return []

#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT F.Fine_ID, F.Issue_ID,
#                    F.Fine_Type, F.Amount, F.Status,
#                    I.Book_ID, B.Title
#             FROM Fines F
#             JOIN Issue_Records I ON F.Issue_ID = I.Issue_ID
#             JOIN Books B ON I.Book_ID = B.Book_ID
#             WHERE I.User_ID = %s
#             ORDER BY F.Fine_ID DESC
#         """, (user_id,))

#         return cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()


# def get_all_fines():

#     connection = connect_database()

#     if connection is None:
#         return []

#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT F.Fine_ID, F.Issue_ID,
#                    F.Fine_Type, F.Amount, F.Status,
#                    I.User_ID, U.First_Name, U.Last_Name,
#                    B.Title
#             FROM Fines F
#             JOIN Issue_Records I ON F.Issue_ID = I.Issue_ID
#             JOIN Users U ON I.User_ID = U.User_ID
#             JOIN Books B ON I.Book_ID = B.Book_ID
#             ORDER BY F.Fine_ID DESC
#         """)

#         return cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()


# def get_outstanding_balance(user_id):

#     connection = connect_database()

#     if connection is None:
#         return 0

#     cursor = connection.cursor()

#     try:
#         cursor.execute("""
#             SELECT COALESCE(SUM(F.Amount), 0)
#             FROM Fines F
#             JOIN Issue_Records I ON F.Issue_ID = I.Issue_ID
#             WHERE I.User_ID = %s
#             AND F.Status = 'UNPAID'
#         """, (user_id,))

#         return cursor.fetchone()[0]

#     finally:
#         cursor.close()
#         connection.close()


# def mark_fine_paid(fine_id):

#     connection = connect_database()

#     if connection is None:
#         return False

#     cursor = connection.cursor()

#     try:
#         cursor.execute("""
#             UPDATE Fines
#             SET Status = 'PAID'
#             WHERE Fine_ID = %s
#             AND Status = 'UNPAID'
#         """, (fine_id,))

#         connection.commit()
#         return cursor.rowcount > 0

#     except Exception as error:
#         connection.rollback()
#         print(error)
#         return False

#     finally:
#         cursor.close()
#         connection.close()



from database.connection import connect_database


def get_member_fines(user_id):

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                F.fine_id AS Fine_ID,
                F.issue_id AS Issue_ID,
                F.fine_type AS Fine_Type,
                F.fine_amount AS Amount,
                F.payment_status AS Status,
                F.fine_date AS Fine_Date,
                I.book_id AS Book_ID,
                B.book_name AS Title
            FROM Fines F
            JOIN Issue_Records I ON F.issue_id = I.issue_id
            JOIN Books B ON I.book_id = B.book_id
            WHERE I.user_id = %s
            ORDER BY F.fine_id DESC
        """, (user_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_all_fines():

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                F.fine_id AS Fine_ID,
                F.issue_id AS Issue_ID,
                F.fine_type AS Fine_Type,
                F.fine_amount AS Amount,
                F.payment_status AS Status,
                I.user_id AS User_ID,
                U.first_name AS First_Name,
                U.last_name AS Last_Name,
                B.book_name AS Title
            FROM Fines F
            JOIN Issue_Records I ON F.issue_id = I.issue_id
            JOIN Users U ON I.user_id = U.user_id
            JOIN Books B ON I.book_id = B.book_id
            ORDER BY F.fine_id DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_outstanding_balance(user_id):

    connection = connect_database()

    if connection is None:
        return 0

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT COALESCE(SUM(F.fine_amount), 0)
            FROM Fines F
            JOIN Issue_Records I ON F.issue_id = I.issue_id
            WHERE I.user_id = %s
              AND F.payment_status = 'PENDING'
        """, (user_id,))

        return cursor.fetchone()[0]

    finally:
        cursor.close()
        connection.close()


def mark_fine_paid(fine_id):

    connection = connect_database()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE Fines
            SET payment_status = 'PAID',
                payment_date = CURDATE()
            WHERE fine_id = %s
              AND payment_status = 'PENDING'
        """, (fine_id,))

        connection.commit()
        return cursor.rowcount > 0

    except Exception as error:
        connection.rollback()
        print(error)
        return False

    finally:
        cursor.close()
        connection.close()