# Import the required libraries
import sys
import requests

# These red lines are expected and pytest will work
sys.path.append(sys.path[0] + '/..')
from config.secrets import API_NINJAS_KEY


def get_baby_names(*, gender: str = "neutral", popular_only: str = "true") -> str:
    """
    Send a GET request to the api-ninjas API using the selected gender and popular status

    :param gender: (str) a specified gender (must be boy, girl, or neutral)
    :param popular_only: (str) whether to only return popular (top 10%) of names (must betrue or false)

    :return: a formatted string of 10 baby names separated by a new line
    """
    # Set up the API URL with our set params
    api_url = 'https://api.api-ninjas.com/v1/babynames?gender={}&{}'.format(gender, popular_only)

    # Send the GET request the defined URL and our personal authorization
    response = requests.get(api_url, headers={'X-Api-Key': API_NINJAS_KEY})

    # Check if the request was successful
    if response.status_code == requests.codes.ok:
        # Return the formatted response
        return format_api_response(text=response.text)
    else:
        # Raise an exception on why the request was unsuccessful
        error_message = f"API Request Status Code: {response.status_code}. API Request Error: {response.text}."
        print(error_message)
        raise Exception(error_message)


def format_api_response(text: str) -> str:
    """
    Receive a list in the form of a string and transform it into user-friendly message

    :param text: (str) a list of strings

    :return: the list of strings separated by a new line
    """
    # Remove the supporting list characters
    remove_extras = text.replace("[", "").replace("]", "").replace('"', '').replace(" ", "")

    # Create a list with the new string
    name_list = remove_extras.split(",")

    # Change the list back into a string separated by new lines
    return "\n".join(name_list)


def check_gender(gender: str = None) -> bool:
    """
    Determine if the gender input is valid

    :param gender: the name of a valid gender

    :return: True if the gender was not provided or an acceptable gender, otherwise, False
    """
    if not gender:
        return True
    elif gender in ("boy", "girl", "neutral"):
        return True
    else:
        return False


def main():
    # args is a list of the command line arguments
    args = sys.argv[1:]

    # Check if the gender argument was provided
    gender = str(args[0]).lower() if len(args) > 0 else None

    # Check if the popular only argument was provided
    popular_only = str(args[1]).lower() if len(args) > 1 else None

    # Verify that the gender input was either not given or valid
    if not check_gender(gender):
        # Since the input was invalid, display a message and reset the gender variable
        print("Gender must be one of the following options: boy, girl, or neutral.")
        gender = None

    # Verify that the popular only input was either not given or valid
    if popular_only and popular_only not in ("true", "false"):
        # Since the input was invalid, display a message and reset the popular_only variable
        print("Popular Only must be one of the following options: true or false.")
        popular_only = None

    # Continue looping until the user wishes to stop
    while True:

        # If the gender was not initially provided or was invalid, loop until a valid gender is given
        while gender is None:
            # Ask the user for an acceptable gender
            gender_input = input("What gender names would you like to look for (boy, girl, or neutral)? ")

            # Check if the gender entered is valid
            if check_gender(gender_input):
                # Set the gender variable since the gender input was an acceptable value
                gender = gender_input
            else:
                # Since the input was invalid, display a message and reset the gender variable
                print("Gender must be one of the following options: boy, girl, or neutral.\n")
                gender = None

        # If the popular only var was not initially provided or was invalid, ask the user
        if not popular_only:
            # Ask the user for the popular only status
            popular_input = input("Would you like only popular names (top 10% of names)? ")

            # Check if their response was yes or anything else and set the popular_only variable accordingly
            if popular_input in ("yes", "y", "1"):
                popular_only = "true"
            else:
                popular_only = "false"

        # Call the API
        names = get_baby_names(gender=gender, popular_only=popular_only)

        # Format the title
        popular_str = "Popular" if popular_only == "true" else "Random"
        print(f"\n<---------- 10 {popular_str} Baby {gender.capitalize()} Names ---------->")

        # Print the names received from the API
        print(f"{names}\n\n")

        # Check if the user would like to stop the program
        more_input = input("Would you like more names? ")
        if more_input not in ("yes", "y", "1"):
            # Break out of the infinite while loop
            break

        # Check if the user wants to use the previously entered gender
        same_gender_input = input("Would you like to keep the same gender? ")
        if same_gender_input not in ("yes", "y", "1"):
            gender = None

        # Check if the user wants to use the previously entered popular only status
        same_popular_input = input("Would you like to keep the same popularity status? ")
        if same_popular_input not in ("yes", "y", "1"):
            popular_only = None

        # Extra line for formatting
        print()

    # Print a final message to the user
    print("\nHave a great day!")


if __name__ == "__main__":
    # Run the main function
    main()
