# Import the required libraries
import io
import sys
import unittest
import pytest
from unittest.mock import patch
from datetime import datetime

# These red lines are expected and pytest will work
sys.path.append(sys.path[0] + '/..')
from custom_object import Employee, get_datetime, main


# To run the tests, execute the following code in the terminal :
#   pytest advanced/tests/test_custom_object.py

# To run the tests and show more output, execute the following code in the terminal : 
#   pytest -vvv advanced/tests/test_custom_object.py

class TestEmployee(unittest.TestCase):
    """ Test the functions within the Employee class """

    def setUp(self):
        """ Run this code before every test """
        # Mock the function that gets datetime.now, therefore, we know what date to expect everytime it is called
        self.mock_datetime = patch("custom_object.get_datetime", return_value=datetime(2011, 11, 11, 11, 11, 11))
        
        # Start the mocks
        self.mock_datetime.start()

        # Define any re-useable variables
        self.employee = Employee(first_name="Lizzie", last_name="Altena", age=25, salary=1000)

        # Capture all printed statements here instead of the terminal
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput

    def tearDown(self):
        """ Run this code after every test """
        # Stop mocking datetime
        self.mock_datetime.stop()

        # Change the print statements to go back to outputting on the terminal
        sys.stdout = sys.__stdout__

    def test_employee_init(self):
        """ Test if the employee init function works properly """
        # Verify that these values were set up correctly using the Employee created in setUp
        assert self.employee.full_name == "Lizzie Altena"
        assert self.employee.age == 25
        assert self.employee.salary == 1000
        assert self.employee.email == ""
        assert self.employee.created_datetime == datetime(2011, 11, 11, 11, 11, 11)
        assert self.employee.updated_datetime is None

    def test_employee_str_repr(self):
        """ Test if the employee __str__ and __repr__ functions work properly """
        # Using the repr function on the employee will also call str
        assert repr(self.employee) == (
            "\n------------ Employee Information ------------\n" +
            f"Name: {self.employee.full_name}\n" +
            f"Age: {self.employee.age}\n" +
            f"Salary: {self.employee.salary}\n" +
            f"Created Date: {self.employee.created_datetime.strftime('%B %d, %Y at %H:%M:%S')}\n"
        )

    def test_employee_eq(self):
        """ Test if the employee __eq__ function works properly """
        # Create a new employee variable with the same paramertes to compare against the first one
        employee_new = Employee(first_name="Lizzie", last_name="Altena", age=25, salary=1000)

        # Using == will call the function __eq__
        assert self.employee == employee_new
    
    def test_display_company_message(self):
        """ Test that the correct message is printed out """
        # Call the tested function
        self.employee.display_company_message()

        # Verify that the captured print output is what was expected
        assert self.capturedOutput.getvalue() == "Welcome to our company, just where you belong!\n\n"

    def test_greet_employee(self):
        """ Test that the correct message is printed out """
        # Call the tested function
        self.employee.greet_employee()

        # Verify that the captured print output is what was expected
        assert self.capturedOutput.getvalue() == (
            f"Hello {self.employee.full_name}! I see you are {self.employee.age}, great to meet you!\n\n"
        )
    
    # When input is called, it will grab this value instead of asking the user
    @patch("builtins.input", return_value='test@test.com')
    def test_retrieve_email_success(self, valid_input):
        # Call the tested function
        self.employee.retrieve_email()

        # Verify that the patched function was called only one time
        valid_input.assert_called_once_with("What is your email? ")

        # Verify that these values were set correctly
        assert self.employee.email == "test@test.com"
        assert self.employee.updated_datetime == datetime(2011, 11, 11, 11, 11, 11)

    def test_retrieve_email_fail_once(self):
        # The input function will be called twice since the first input is not valid, this sets up both inputs
        mock_inputs = ['test', 'test@test.com']

        # Change the real input function to use a fake input function
        with patch('builtins.input') as mocked_input:

            # Change the fake input function's returns to use our mock_inputs
            mocked_input.side_effect = mock_inputs

            # Call the tested function
            self.employee.retrieve_email()
        
        # Verify that these values were set correctly
        assert self.employee.email == "test@test.com"
        assert self.employee.updated_datetime == datetime(2011, 11, 11, 11, 11, 11)


# Test the main functions
class TestMain(unittest.TestCase):
    def test_get_datetime(self):
        """
        The function, get_datetime, wrapped the datetime now function for easier mocking. 
        Standard methods of mocking are not simple for libraries implemented in C due to the following error: 
        TypeError: can't set attributes of built-in/extension type 'datetime.datetime'.
        """
        # Call the tested function
        current_datetime = get_datetime()

        # Verify that a datetime was returned, unable to check value because it changes
        assert isinstance(current_datetime, datetime)

    # Instead of actually calling the functions, change it so nothing happens instead
    @patch.object(Employee, "display_company_message")
    @patch.object(Employee, "greet_employee")
    @patch.object(Employee, "retrieve_email")
    def test_main_success(self, valid_message, valid_greeting, valid_email):
        """
        Test the main function with valid args
        """
        # Mock the arguments
        sys.argv = ["11-Custom_Objects.py", "Lizzie", "Altena", 25, 100000]

        # Call the tested function
        main()

        # Verify that the functions were called
        valid_message.assert_called() 
        valid_greeting.assert_called() 
        valid_email.assert_called() 

    def test_main_fail(self):
        """
        Test the main function with no args
        """
        # Verify that providing no args raises an error
        with pytest.raises(Exception):   
            # Call the tested function
            main()
        