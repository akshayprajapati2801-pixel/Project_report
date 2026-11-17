# ==========================================
# Create Admin User
# ==========================================

from getpass import getpass

from services.auth_service import AuthService


def main():

    print("==========================================")
    print("Hospital Management System")
    print("Create Admin User")
    print("==========================================")

    username = input("Enter admin username: ").strip()

    full_name = input("Enter full name: ").strip()

    password = getpass("Enter password: ")

    confirm_password = getpass(
        "Confirm password: "
    )

    if password != confirm_password:

        print()
        print("Passwords do not match.")
        return

    auth_service = AuthService()

    success, message = auth_service.register(
        username=username,
        password=password,
        full_name=full_name,
        role="admin"
    )

    print()
    print("==========================================")
    print(message)
    print("==========================================")


if __name__ == "__main__":
    main()