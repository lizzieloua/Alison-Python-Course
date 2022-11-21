# Import the required libraries
import sys
import requests
import shutil

from PIL import Image

from config.secrets import API_NINJAS_KEY, IMAGE_FILE


def get_random_image(*, category: str = "nature", width: str = "3072", height: str = "1920"):
    """
    Send a GET request to the api-ninjas API using the selected category to get a random image

    :param category: (str) a category for image theme (nature, city, technology, food, still_life, abstract, wildlife)
    :param width: (str) the desired width of the image
    :param height: (str) the desired height of the image

    :return: a random image file based on the selected category
    """
    # Set up the API URL with our set params
    api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}&width={}&height={}'.format(category, width, height)

    # Send the GET request the defined URL and our personal authorization
    response = requests.get(api_url, headers={'X-Api-Key': API_NINJAS_KEY, 'Accept': 'image/jpg'}, stream=True)

    # Check if the request was successful
    if response.status_code == requests.codes.ok:
        # Save the image locally
        with open(IMAGE_FILE, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

    else:
        # Raise an exception on why the request was unsuccessful
        error_message = f"API Request Status Code: {response.status_code}. API Request Error: {response.text}."
        print(error_message)
        raise Exception(error_message)


def check_category(category: str = None) -> bool:
    """
    Determine if the category input is valid

    :param category: the name of a valid category

    :return: True if the category was not provided or an acceptable category, otherwise, False
    """
    # If a category was not provided, return True
    if not category:
        return True
    # If the category was one of the valid options, return True
    elif category in ("nature", "city", "technology", "food", "still_life", "abstract", "wildlife"):
        return True
    # Return False for anything else
    else:
        return False


def main():
    # args is a list of the command line arguments
    args = sys.argv[1:]

    # Check if the category argument was provided
    category = str(args[0]).lower() if len(args) > 0 else None

    # Verify that the category input was either not given or valid
    if not check_category(category):
        # Since the input was invalid, display a message and reset the category variable
        print(
            "Category must be one of the following options: "
            "nature, city, technology, food, still_life, abstract, or wildlife."
        )
        category = None

    # Continue looping until the user wishes to stop
    while True:

        # If the category was not initially provided or was invalid, loop until a valid category is given
        while category is None:

            # Ask the user for an acceptable category
            category_input = input(
                "What theme do you want for your image "
                "(nature, city, technology, food, still_life, abstract, or wildlife)? "
            )

            # Check if the category entered is valid
            if check_category(category_input):

                # Set the category variable since the category input was an acceptable value
                category = category_input
            else:
                # Since the input was invalid, display a message and reset the category variable
                print(
                    "Category must be one of the following options: "
                    "nature, city, technology, food, still_life, abstract, or wildlife.\n"
                )
                category = None

        # Call the API
        get_random_image(category=category)

        # Open the new file
        image = Image.open(IMAGE_FILE)
        image.show()

        # Check if the user would like to stop the program
        more_input = input("Would you like a different image? ")
        if more_input not in ("yes", "y", "1"):

            # Break out of the infinite while loop
            break

        # Check if the user wants to use the previously entered category
        same_category_input = input("Would you like to keep the same category? ")
        if same_category_input not in ("yes", "y", "1"):

            # Reset the category variable
            category = None

        # Extra line for formatting
        print()

    # Check if the user would like to change their desktop background
    desktop_input = input("\nWould you like to use the previously shown image as your desktop background? ")
    if desktop_input in ("yes", "y", "1"):

        # Move the file to the Pictures folder
        shutil.move(IMAGE_FILE, "../../../Pictures/new_desktop_picture.jpg")

        # Provide instructions
        print(
            "\nPlease follow these instructions:\n"
            "1. Open System Preferences > Desktop & Screen Saver\n"
            "2. Make sure you’re in the Desktop tab\n"
            "3. In the sidebar, open Folders > Pictures\n"
            "4. Click on the new picture (new_desktop_picture.jpg) to set it as your background."
        )

    # Print a final message to the user
    print("\nHave a great day!")


if __name__ == "__main__":
    # Run the main function
    main()
