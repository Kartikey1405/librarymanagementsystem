# import hashlib
# import hmac
# import os
# from datetime import date

# from database.connection import connect_database


# def hash_password(password):

#     salt = os.urandom(16)

#     digest = hashlib.pbkdf2_hmac(
#         "sha256",
#         password.encode("utf-8"),
#         salt,
#         100000
#     )

#     return salt.hex() + ":" + digest.hex()


# def verify_password(password, stored_hash):

#     try:

#         salt_hex, digest_hex = stored_hash.split(":")

#         salt = bytes.fromhex(salt_hex)

#         digest = hashlib.pbkdf2_hmac(
#             "sha256",
#             password.encode("utf-8"),
#             salt,
#             100000
#         )

#         return hmac.compare_digest(
#             digest.hex(),
#             digest_hex
#         )

#     except (ValueError, AttributeError):
#         return False


# def register_user(user_id, first_name, last_name,
#                   email, phone, password, role):

#     # Public registration is only for students and teachers.
#     if role not in ("STUDENT", "TEACHER"):
#         return False, "Invalid registration role."

#     if not all([user_id, first_name, last_name, email, password]):
#         return False, "Please fill in all required fields."

#     if len(password) < 6:
#         return False, "Password must contain at least 6 characters."

#     connection = connect_database()

#     if connection is None:
#         return False, "Database connection failed."

#     cursor = None

#     try:

#         cursor = connection.cursor()

#         password_hash = hash_password(password)

#         query = """
#             INSERT INTO Users
#             (user_id, first_name, last_name, email,
#              phone, password_hash, role, joining_date)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """

#         values = (
#             user_id,
#             first_name,
#             last_name,
#             email,
#             phone,
#             password_hash,
#             role,
#             date.today()
#         )

#         cursor.execute(query, values)
#         connection.commit()

#         return True, "Registration successful."

#     except Exception as error:

#         connection.rollback()
#         return False, str(error)

#     finally:

#         if cursor:
#             cursor.close()

#         connection.close()


# def login_user(user_id, password):

#     connection = connect_database()

#     if connection is None:
#         return None

#     cursor = None

#     try:

#         cursor = connection.cursor(dictionary=True)

#         cursor.execute(
#             "SELECT * FROM Users WHERE user_id = %s",
#             (user_id,)
#         )

#         user = cursor.fetchone()

#         if user and verify_password(
#             password,
#             user["password_hash"]
#         ):
#             return user

#         return None

#     except Exception as error:

#         print("Login error:", error)
#         return None

#     finally:

#         if cursor:
#             cursor.close()

#         connection.close()


# def create_librarian(user_id, first_name, last_name,
#                      email, phone, password):

#     if not all([user_id, first_name, last_name, email, password]):
#         return False, "Please fill in all required fields."

#     if len(password) < 6:
#         return False, "Password must contain at least 6 characters."

#     connection = connect_database()

#     if connection is None:
#         return False, "Database connection failed."

#     cursor = None

#     try:

#         cursor = connection.cursor()

#         cursor.execute(
#             """
#             INSERT INTO Users
#             (user_id, first_name, last_name, email,
#              phone, password_hash, role, joining_date)
#             VALUES (%s, %s, %s, %s, %s, %s, 'LIBRARIAN', %s)
#             """,
#             (
#                 user_id,
#                 first_name,
#                 last_name,
#                 email,
#                 phone,
#                 hash_password(password),
#                 date.today()
#             )
#         )

#         connection.commit()

#         return True, "Librarian account created successfully."

#     except Exception as error:

#         connection.rollback()
#         return False, str(error)

#     finally:

#         if cursor:
#             cursor.close()

#         connection.close()
import hashlib
import hmac
import os
from datetime import date

from database.connection import connect_database


def hash_password(password):
    salt = os.urandom(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return salt.hex() + ":" + hashed.hex()


def verify_password(password, stored_password):
    try:
        salt_hex, hash_hex = stored_password.split(":")
        salt = bytes.fromhex(salt_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return hmac.compare_digest(new_hash.hex(), hash_hex)

    except (ValueError, AttributeError):
        return False


def register_user(user_id, first_name, last_name, email,
                  phone, password, role):

    if role not in ("STUDENT", "TEACHER"):
        return False, "Invalid role."

    if not all([user_id, first_name, last_name, email, password]):
        return False, "Please fill all required fields."

    if len(user_id) > 12:
        return False, "User ID cannot exceed 12 characters."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    connection = connect_database()

    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT user_id FROM Users WHERE user_id = %s",
            (user_id,)
        )

        if cursor.fetchone():
            return False, "This User ID is already registered."

        password_hash = hash_password(password)

        cursor.execute("""
            INSERT INTO Users
            (user_id, first_name, last_name, email, phone,
             password_hash, role, joining_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            first_name,
            last_name,
            email,
            phone or None,
            password_hash,
            role,
            date.today()
        ))

        connection.commit()
        return True, "Registration successful."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        cursor.close()
        connection.close()


def login_user(user_id, password):

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
                password_hash AS Password,
                role AS Role,
                joining_date AS Joining_Date
            FROM Users
            WHERE user_id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if user and verify_password(password, user["Password"]):
            return user

        return None

    except Exception as error:
        print("Login error:", error)
        return None

    finally:
        cursor.close()
        connection.close()


def create_librarian(user_id, first_name, last_name, email,
                     phone, password):

    connection = connect_database()

    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor()

    try:
        if len(user_id) > 12:
            return False, "Librarian ID cannot exceed 12 characters."

        if len(password) < 6:
            return False, "Password must contain at least 6 characters."

        cursor.execute(
            "SELECT user_id FROM Users WHERE user_id = %s",
            (user_id,)
        )

        if cursor.fetchone():
            return False, "This User ID already exists."

        password_hash = hash_password(password)

        cursor.execute("""
            INSERT INTO Users
            (user_id, first_name, last_name, email, phone,
             password_hash, role, joining_date)
            VALUES (%s, %s, %s, %s, %s, %s, 'LIBRARIAN', %s)
        """, (
            user_id,
            first_name,
            last_name,
            email,
            phone or None,
            password_hash,
            date.today()
        ))

        connection.commit()
        return True, "Librarian account created successfully."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        cursor.close()
        connection.close()