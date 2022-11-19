# Import the required libraries
import sys

from datetime import datetime

class Employee:

    # An employee's full name
    full_name = ""

    # An employee's age
    age = 0

    # An employee's salary
    salary = 0

    # An employee's email
    email = ""

    # The date time the employee was created
    created_datetime = None

    # The date time the employee was updated
    updated_datetime = None


    def __init__(
        self, 
        *,
        first_name: str,
        last_name: str,
        age: int,
        salary: int, 
        email: str = ""
        ):

        # Display a message to track code progress
        print("Creating a new employee!")

        # Set up the object variables using the information given
        self.full_name = first_name.capitalize() + " " + last_name.capitalize()
        self.age = age
        self.salary = salary
        self.email = email

        # Store the current date in created_date
        self.created_datetime = get_datetime()

    def __str__(self) -> str:
        """ Override the string function to format it appropiately """
        return (
            "\n------------ Employee Information ------------\n" +
            f"Name: {self.full_name}\n" +
            f"Age: {self.age}\n" +
            f"Salary: {self.salary}\n" +
            (f"Email: {self.email}\n" if self.email else "") +
            f"Created Date: {self.created_datetime.strftime('%B %d, %Y at %H:%M:%S')}\n" +
            (f"Updated Date: {self.updated_datetime.strftime('%B %d, %Y at %H:%M:%S')}\n" if self.updated_datetime else "")
        )

    def __repr__(self) -> str:
        """ Override the internal representation to use our overriden str message """
        return str(self)

    def __eq__(self, target) -> bool:
        """ Override the equal to compare our overriden str message """
        return str(self) == str(target)

    @staticmethod
    def display_company_message() -> None:
        """ This function is generic for every employee. Therefore, it can be static because it does not require employee information. """
        print("Welcome to our company, just where you belong!\n")

    def greet_employee(self) -> None:
        """ This function displays a nice message for the employee """
        print(f"Hello {self.full_name}! I see you are {self.age}, great to meet you!\n")

    def retrieve_email(self) -> None:
        """ This function asks the employee for their email """

        # Ask the employee for their email until valid input is received
        while True:
            # Gather their input
            emailResponse = input("What is your email? ")

            # Check if the input is valid
            if "@" in emailResponse and "." in emailResponse:
                # Since the email provided was valid, break out of the while loop
                break
            else:
                # Since the email provided was invalid, ask the employee again
                print(f"The email given, {emailResponse}, is not valid. Please provide a valid email.\n")
        
        # The email must be valid to get here
        self.email = emailResponse

        # Update the updated_datetime variable
        self.updated_datetime = get_datetime()


def main():
    # args is a list of the command line arguments, starts at index 1 because index 0 is the file name
    args = sys.argv[1:]

    # We expect 4 arguments, raise an exception if not provided
    if len(args) != 4:
        raise Exception("This program expects 4 arguments.\nPlease try re-running the program and provide first name, last name, age, and salary.")

    # Create a variable using the custom object, Employee
    employee = Employee(first_name=args[0], last_name=args[1], age=args[2], salary=args[3])

    # Display the employee's initial information
    print(employee)

    # Display the company message for the employee
    employee.display_company_message()

    # Display a greeting
    employee.greet_employee()

    # Ask the user for their information
    employee.retrieve_email()

    # Display the employee's updated information
    print(employee)


def get_datetime() -> datetime:
    """ 
    Return the current datetime
    """
    return datetime.now()


if __name__ == "__main__":
    main()

