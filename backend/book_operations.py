# from database.connection import connect_database


# def add_book(book_id, title, author, category,
#              publisher, total_copies):

#     connection = connect_database()

#     if connection is None:
#         return False, "Database connection failed."

#     cursor = connection.cursor()

#     try:
#         cursor.execute("""
#             INSERT INTO Books
#             (Book_ID, Title, Author, Category,
#              Publisher, Total_Copies, Available_Copies)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """, (
#             book_id,
#             title,
#             author,
#             category,
#             publisher,
#             total_copies,
#             total_copies
#         ))

#         connection.commit()
#         return True, "Book added successfully."

#     except Exception as error:
#         connection.rollback()
#         return False, str(error)

#     finally:
#         cursor.close()
#         connection.close()


# def get_all_books():

#     connection = connect_database()

#     if connection is None:
#         return []

#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("SELECT * FROM Books ORDER BY Title")
#         return cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()


# def search_book(search_text):

#     connection = connect_database()

#     if connection is None:
#         return []

#     cursor = connection.cursor(dictionary=True)

#     try:
#         search_value = "%" + search_text + "%"

#         cursor.execute("""
#             SELECT * FROM Books
#             WHERE Book_ID LIKE %s
#             OR Title LIKE %s
#             OR Author LIKE %s
#             OR Category LIKE %s
#         """, (
#             search_value,
#             search_value,
#             search_value,
#             search_value
#         ))

#         return cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()


# def update_book(book_id, title, author, category,
#                 publisher, total_copies):

#     connection = connect_database()

#     if connection is None:
#         return False, "Database connection failed."

#     cursor = connection.cursor()

#     try:
#         cursor.execute("""
#             SELECT COUNT(*)
#             FROM Issue_Records
#             WHERE Book_ID = %s AND Status = 'ISSUED'
#         """, (book_id,))

#         issued_copies = cursor.fetchone()[0]

#         if total_copies < issued_copies:
#             return False, "Total copies cannot be less than issued copies."

#         available_copies = total_copies - issued_copies

#         cursor.execute("""
#             UPDATE Books
#             SET Title = %s,
#                 Author = %s,
#                 Category = %s,
#                 Publisher = %s,
#                 Total_Copies = %s,
#                 Available_Copies = %s
#             WHERE Book_ID = %s
#         """, (
#             title,
#             author,
#             category,
#             publisher,
#             total_copies,
#             available_copies,
#             book_id
#         ))

#         connection.commit()
#         return cursor.rowcount > 0, "Book updated."

#     except Exception as error:
#         connection.rollback()
#         return False, str(error)

#     finally:
#         cursor.close()
#         connection.close()


# def delete_book(book_id):

#     connection = connect_database()

#     if connection is None:
#         return False, "Database connection failed."

#     cursor = connection.cursor()

#     try:
#         cursor.execute(
#             "DELETE FROM Books WHERE Book_ID = %s",
#             (book_id,)
#         )

#         connection.commit()
#         return cursor.rowcount > 0, "Book deleted."

#     except Exception as error:
#         connection.rollback()
#         return False, "Book cannot be deleted because it has transaction records."

#     finally:
#         cursor.close()
#         connection.close()


from database.connection import connect_database


def add_book(book_name, author, category, publisher, total_copies):

    if total_copies <= 0:
        return False, "Total copies must be greater than zero."

    connection = connect_database()

    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO Books
            (book_name, author, category, publisher,
             total_copies, available_copies)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            book_name,
            author,
            category,
            publisher,
            total_copies,
            total_copies
        ))

        connection.commit()
        return True, "Book added successfully."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        cursor.close()
        connection.close()


def get_all_books():

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                book_id AS Book_ID,
                book_name AS Title,
                author AS Author,
                category AS Category,
                publisher AS Publisher,
                total_copies AS Total_Copies,
                available_copies AS Available_Copies
            FROM Books
            ORDER BY book_name
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def search_book(search_text):

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        search_value = "%" + search_text + "%"

        cursor.execute("""
            SELECT
                book_id AS Book_ID,
                book_name AS Title,
                author AS Author,
                category AS Category,
                publisher AS Publisher,
                total_copies AS Total_Copies,
                available_copies AS Available_Copies
            FROM Books
            WHERE CAST(book_id AS CHAR) LIKE %s
               OR book_name LIKE %s
               OR author LIKE %s
               OR category LIKE %s
            ORDER BY book_name
        """, (
            search_value,
            search_value,
            search_value,
            search_value
        ))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def update_book(book_id, book_name, author, category,
                publisher, total_copies):

    connection = connect_database()

    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM Issue_Records
            WHERE book_id = %s AND status = 'ISSUED'
        """, (book_id,))

        issued_copies = cursor.fetchone()[0]

        if total_copies < issued_copies or total_copies <= 0:
            return False, "Invalid total copies."

        available_copies = total_copies - issued_copies

        cursor.execute("""
            UPDATE Books
            SET book_name = %s,
                author = %s,
                category = %s,
                publisher = %s,
                total_copies = %s,
                available_copies = %s
            WHERE book_id = %s
        """, (
            book_name,
            author,
            category,
            publisher,
            total_copies,
            available_copies,
            book_id
        ))

        connection.commit()

        if cursor.rowcount > 0:
            return True, "Book updated successfully."

        return False, "Book not found."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        cursor.close()
        connection.close()


def delete_book(book_id):

    connection = connect_database()

    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM Books WHERE book_id = %s",
            (book_id,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            return True, "Book deleted successfully."

        return False, "Book not found."

    except Exception:
        connection.rollback()
        return False, "Book cannot be deleted because transaction records exist."

    finally:
        cursor.close()
        connection.close()