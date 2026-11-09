from getpass import getpass

from backend.authentication import create_librarian


print("\n================================")
print("   CREATE LIBRARIAN ACCOUNT")
print("================================\n")


user_id = input("Librarian ID: ").strip()

first_name = input("First Name: ").strip()

last_name = input("Last Name: ").strip()

email = input("Email: ").strip()

phone = input("Phone Number: ").strip()

password = getpass("Password: ")

confirm_password = getpass("Confirm Password: ")


if password != confirm_password:

    print("\nPasswords do not match.")

else:

    success, message = create_librarian(
        user_id,
        first_name,
        last_name,
        email,
        phone,
        password
    )

    print("\n" + message)