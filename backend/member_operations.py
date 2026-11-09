# from database.connection import connect_database


# def get_all_members():

#     connection = connect_database()

#     if connection is None:
#         return []

#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT User_ID, First_Name, Last_Name,
#                    Email, Phone, Role
#             FROM Users
#             WHERE Role IN ('STUDENT', 'TEACHER')
#             ORDER BY First_Name
#         """)

#         return cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()


# def get_member(user_id):

#     connection = connect_database()

#     if connection is None:
#         return None

#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT User_ID, First_Name, Last_Name,
#                    Email, Phone, Role
#             FROM Users
#             WHERE User_ID = %s
#             AND Role IN ('STUDENT', 'TEACHER')
#         """, (user_id,))

#         return cursor.fetchone()

#     finally:
#         cursor.close()
#         connection.close()


# def update_member(user_id, first_name, last_name, email, phone):

#     connection = connect_database()

#     if connection is None:
#         return False

#     cursor = connection.cursor()

#     try:
#         cursor.execute("""
#             UPDATE Users
#             SET First_Name = %s,
#                 Last_Name = %s,
#                 Email = %s,
#                 Phone = %s
#             WHERE User_ID = %s
#             AND Role IN ('STUDENT', 'TEACHER')
#         """, (first_name, last_name, email, phone, user_id))

#         connection.commit()
#         return cursor.rowcount > 0

#     except Exception as error:
#         connection.rollback()
#         print(error)
#         return False

#     finally:
#         cursor.close()
#         connection.close()


# def delete_member(user_id):

#     connection = connect_database()

#     if connection is None:
#         return False

#     cursor = connection.cursor()

#     try:
#         cursor.execute("""
#             DELETE FROM Users
#             WHERE User_ID = %s
#             AND Role IN ('STUDENT', 'TEACHER')
#         """, (user_id,))

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


def get_all_members():

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                user_id AS User_ID,
                first_name AS First_Name,
                last_name AS Last_Name,
                email AS Email,
                phone AS Phone,
                role AS Role
            FROM Users
            WHERE role IN ('STUDENT', 'TEACHER')
            ORDER BY first_name
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_member(user_id):

    connection = connect_database()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                user_id AS User_ID,
                first_name AS First_Name,
                last_name AS Last_Name,
                email AS Email,
                phone AS Phone,
                role AS Role
            FROM Users
            WHERE user_id = %s
              AND role IN ('STUDENT', 'TEACHER')
        """, (user_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def update_member(user_id, first_name, last_name, email, phone):

    connection = connect_database()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE Users
            SET first_name = %s,
                last_name = %s,
                email = %s,
                phone = %s
            WHERE user_id = %s
              AND role IN ('STUDENT', 'TEACHER')
        """, (
            first_name,
            last_name,
            email,
            phone or None,
            user_id
        ))

        connection.commit()
        return cursor.rowcount > 0

    except Exception as error:
        connection.rollback()
        print(error)
        return False

    finally:
        cursor.close()
        connection.close()


def delete_member(user_id):

    connection = connect_database()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM Users
            WHERE user_id = %s
              AND role IN ('STUDENT', 'TEACHER')
        """, (user_id,))

        connection.commit()
        return cursor.rowcount > 0

    except Exception as error:
        connection.rollback()
        print(error)
        return False

    finally:
        cursor.close()
        connection.close()