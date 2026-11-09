
# # ==========================================
# # LIBRARY MANAGEMENT SYSTEM
# # MAIN PROGRAM
# # ==========================================

# from database.connection import connect_database


# def main():

#     connection = connect_database()

#     if connection:

#         print("================================")
#         print(" LIBRARY MANAGEMENT SYSTEM")
#         print("================================")

#         print("MySQL Connection Successful!")

#         cursor = connection.cursor()

#         cursor.execute("SELECT DATABASE()")

#         result = cursor.fetchone()

#         print("Connected Database:", result[0])

#         cursor.close()
#         connection.close()

#         print("Connection Closed Successfully.")

#     else:

#         print("Unable to connect to MySQL.")


# if __name__ == "__main__":
#     main()

# ==========================================
# LIBRARY MANAGEMENT SYSTEM
# CLASS XII CBSE COMPUTER SCIENCE PROJECT
# ==========================================

import tkinter as tk
from tkinter import messagebox

from database.connection import connect_database
from gui.home import show_home


def main():

    # Check MySQL database connection
    connection = connect_database()

    if connection is None:

        messagebox.showerror(
            "Database Error",
            "Unable to connect to MySQL.\n"
            "Please check your database connection."
        )

        return

    # Close test connection
    connection.close()

    # Create main application window
    root = tk.Tk()

    root.title("Library Management System")

    root.geometry("950x620")

    root.minsize(800, 550)

    # Display home page
    show_home(root)

    # Start application
    root.mainloop()


if __name__ == "__main__":
    main()
