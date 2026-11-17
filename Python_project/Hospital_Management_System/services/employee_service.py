from repositories.employee_repository import EmployeeRepository


class EmployeeService:

    def __init__(self):
        self.repository = EmployeeRepository()

    def get_all(self):

        return self.repository.get_all()

    def get_by_id(self, employee_id):

        return self.repository.get_by_id(
            employee_id
        )

    def create(
        self,
        name,
        phone,
        email,
        department,
        salary
    ):

        name = name.strip()
        phone = phone.strip()
        email = email.strip()
        department = department.strip()

        if not name:
            return False, "Employee name is required"

        try:

            salary = float(salary)

        except ValueError:

            return False, "Salary must be a number"

        if salary < 0:

            return False, "Salary cannot be negative"

        try:

            self.repository.create(
                name,
                phone,
                email,
                department,
                salary
            )

            return True, "Employee added successfully"

        except Exception as error:

            return False, str(error)

    def update(
        self,
        employee_id,
        name,
        phone,
        email,
        department,
        salary
    ):

        name = name.strip()
        phone = phone.strip()
        email = email.strip()
        department = department.strip()

        if not name:
            return False, "Employee name is required"

        try:

            salary = float(salary)

        except ValueError:

            return False, "Salary must be a number"

        if salary < 0:

            return False, "Salary cannot be negative"

        try:

            self.repository.update(
                employee_id,
                name,
                phone,
                email,
                department,
                salary
            )

            return True, "Employee updated successfully"

        except Exception as error:

            return False, str(error)

    def delete(self, employee_id):

        try:

            self.repository.delete(
                employee_id
            )

            return True, "Employee deleted successfully"

        except Exception as error:

            return False, str(error)