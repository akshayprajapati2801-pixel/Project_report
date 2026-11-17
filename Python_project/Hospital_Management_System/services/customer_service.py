# ==========================================
# Patient / Customer Service
# ==========================================

from repositories.customer_repository import CustomerRepository


class CustomerService:

    def __init__(self):

        self.repository = CustomerRepository()

    # --------------------------------------
    # Get All Patients
    # --------------------------------------

    def get_all(self):

        return self.repository.get_all()

    # --------------------------------------
    # Get Patient
    # --------------------------------------

    def get_by_id(self, customer_id):

        return self.repository.get_by_id(
            customer_id
        )

    # --------------------------------------
    # Add Patient
    # --------------------------------------

    def create(
        self,
        name,
        phone,
        email,
        address,
        age,
        gender
    ):

        name = name.strip()
        phone = phone.strip()
        email = email.strip()
        address = address.strip()
        gender = gender.strip()

        if not name:
            return False, "Patient name is required"

        if age:

            try:
                age = int(age)

            except ValueError:
                return False, "Age must be a number"

            if age <= 0 or age > 120:
                return False, "Enter a valid age"

        else:

            age = None

        try:

            self.repository.create(
                name,
                phone,
                email,
                address,
                age,
                gender
            )

            return True, "Patient added successfully"

        except Exception as error:

            return False, str(error)

    # --------------------------------------
    # Update Patient
    # --------------------------------------

    def update(
        self,
        customer_id,
        name,
        phone,
        email,
        address,
        age,
        gender
    ):

        name = name.strip()
        phone = phone.strip()
        email = email.strip()
        address = address.strip()
        gender = gender.strip()

        if not name:
            return False, "Patient name is required"

        if age:

            try:
                age = int(age)

            except ValueError:
                return False, "Age must be a number"

            if age <= 0 or age > 120:
                return False, "Enter a valid age"

        else:

            age = None

        try:

            self.repository.update(
                customer_id,
                name,
                phone,
                email,
                address,
                age,
                gender
            )

            return True, "Patient updated successfully"

        except Exception as error:

            return False, str(error)

    # --------------------------------------
    # Delete Patient
    # --------------------------------------

    def delete(self, customer_id):

        try:

            self.repository.delete(
                customer_id
            )

            return True, "Patient deleted successfully"

        except Exception as error:

            return False, str(error)