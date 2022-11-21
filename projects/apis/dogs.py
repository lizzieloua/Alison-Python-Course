# Import the required libraries
import requests

# Import the secret key
from config.secrets import API_NINJAS_KEY


def get_dog_options(
        *,
        min_weight: str = None,
        max_weight: str = None,
        min_life_expectancy: str = None,
        max_life_expectancy: str = None,
        shedding: str = None,
        barking: str = None,
        energy: str = None,
        protectiveness: str = None,
        trainability: str = None,
        offset: int = 0
) -> list:
    """
    Send a GET request to the api-ninjas API using the selected dog properties

    :param min_weight: (str) minimum weight in pounds
    :param max_weight (str) - maximum weight in pounds.
    :param min_life_expectancy (str) - minimum life expectancy in years.
    :param max_life_expectancy (str) - maximum life expectancy in years.
    :param shedding (str) - How much hair the breed sheds.
        Possible values: 0, 1, 2, 3, 4, 5, where 0 indicates no shedding and 5 indicates maximum shedding.
    :param barking (str) - How vocal the breed is.
        Possible values: 0, 1, 2, 3, 4, 5, where 0 indicates minimal barking and 5 indicates maximum barking.
    :param energy (str) - How much energy the breed has.
        Possible values: 0, 1, 2, 3, 4, 5, where 0 indicates low energy and 5 indicates high energy.
    :param protectiveness (str) - How likely the breed is to alert strangers.
        Possible values: 0, 1, 2, 3, 4, 5, where 0 indicates minimal alerting and 5 indicates maximum alerting.
    :param trainability (str) - How easy it is to train the breed.
        Possible values: 0, 1, 2, 3, 4, 5, where 0 indicates the breed is very difficult to train
        and 5 indicates the breed is very easy to train
    :param offset: (int) number of results to offset for pagination.

    :return: a list of dogs that matched the criteria provided
    """
    # Set up the API URL with our set params
    api_url = 'https://api.api-ninjas.com/v1/dogs?'

    # Use at least one query param
    api_url += f"min_weight={min_weight or '1'}&"

    # Check to see which query params were provided
    if max_weight:
        api_url += f"max_weight={max_weight}&"
    if min_life_expectancy:
        api_url += f"min_life_expectancy={min_life_expectancy}&"
    if max_life_expectancy:
        api_url += f"max_life_expectancy={max_life_expectancy}&"
    if shedding:
        api_url += f"shedding={shedding}&"
    if barking:
        api_url += f"barking={barking}&"
    if energy:
        api_url += f"energy={energy}&"
    if protectiveness:
        api_url += f"protectiveness={protectiveness}&"
    if trainability:
        api_url += f"trainability={trainability}&"
    if offset:
        api_url += f"offset={offset}&"

    # Remove the last ampersand (&)
    if api_url[-1] == "&":
        api_url = api_url[:-1]

    # Send the GET request the defined URL and our personal authorization
    response = requests.get(api_url, headers={'X-Api-Key': API_NINJAS_KEY})

    # Check if the request was successful
    if response.status_code == requests.codes.ok:
        # Return the formatted response
        return eval(response.text)
    else:
        # Raise an exception on why the request was unsuccessful
        error_message = f"API Request Status Code: {response.status_code}. API Request Error: {response.text}."
        print(error_message)
        raise Exception(error_message)


def get_user_input(variable: str) -> str:
    """
    Receive a variable name and ask the user until a valid input is given

    :param variable: (str) a user-friendly name of a query parameter

    :return: a valid input for the variable or None
    """
    # Format the input message based on the variable
    if variable in ("minimum weight", "maximum weight"):
        # Expecting a number
        is_range = False

        # Displaying a message for a variable looking for pounds
        input_message = f"What would you like the {variable} to be in pounds (NA if you do not care)? "

    elif variable in ("minimum life expectancy", "maximum life expectancy"):
        # Expecting a number
        is_range = False

        # Displaying a message for a variable looking for years
        input_message = f"What would you like the {variable} to be in years (NA if you do not care)? "

    else:
        # Expecting a number between 0 and 5
        is_range = True
        input_message = (
            f"What would you like the {variable} to be on a range from 0 to 5, where 0 is on the "
            f"low end of {variable} and 5 is on the high end (NA if you do not care)? "
        )

    # loop until a valid input is given for the variable
    while True:
        response = input(input_message).lower()

        # Return None if they do not want to consider this variable
        if response == "na":
            return None
        # Make sure the input is valid if the variable is looking for a number 0-5
        elif is_range and response in ("0", "1", "2", "3", "4", "5"):
            return response
        # Make sure the input is a number if it is not a range
        elif not is_range and response.isdigit():
            return response
        else:
            # Did not meet any criteria
            print(f"'{response}' was not a valid input. Please try again.")


def main():
    # Display a welcome message
    print("Welcome to Dog Breed Matcher! Please provide criteria and we'll find dogs that match it!\n")

    # Define variables here to be easily used in the while loop
    back = False
    offset = 0
    min_weight_value = None
    max_weight_value = None
    min_life_expectancy_value = None
    max_life_expectancy_value = None
    shedding_value = None
    barking_value = None
    energy_value = None
    protectiveness_value = None
    trainability_value = None

    # Continue looping until the user wishes to stop
    while True:

        # Ask search criteria if the user is not looking for the previous or next results of the last query
        if not offset and not back:

            # Ask for user input on each variable
            min_weight_value = get_user_input("minimum weight")
            max_weight_value = get_user_input("maximum weight")
            min_life_expectancy_value = get_user_input("minimum life expectancy")
            max_life_expectancy_value = get_user_input("maximum life expectancy")
            shedding_value = get_user_input("shedding")
            barking_value = get_user_input("barking")
            energy_value = get_user_input("energy")
            protectiveness_value = get_user_input("protectiveness")
            trainability_value = get_user_input("trainability")

        # Call the API with the inputs provided
        dogs = get_dog_options(
            min_weight=min_weight_value,
            max_weight=max_weight_value,
            min_life_expectancy=min_life_expectancy_value,
            max_life_expectancy=max_life_expectancy_value,
            shedding=shedding_value,
            barking=barking_value,
            energy=energy_value,
            protectiveness=protectiveness_value,
            trainability=trainability_value,
            offset=offset
        )

        # Check if no dogs were returned due to picky criteria or exactly no dogs left after going to the next page
        if len(dogs) == 0:

            # Display a message explaining the situation
            print("\n<----- No dogs were returned in the search. Starting from the beginning. ----->\n")

            # Reset the loop variables
            offset = 0
            back = False

            # Go to the next iteration of the loop
            continue

        # Format the title
        print(f"\n<---------- {len(dogs)} Dogs Matching Your Criteria ---------->")

        # Print the names received from the API
        names = "\n".join([dog["name"] for dog in dogs])
        print(f"{names}\n\n")

        # Ask if the user wants more information
        info_input = input("Would you like more information on one of the dog breeds? ")

        # Check if they agreed
        if info_input in ("yes", "y", "1"):

            # Check if there was only one dog in the list
            found_dog = dogs[0] if len(dogs) == 1 else None

            # Loop until a valid dog name was entered from the list
            while found_dog is None:
                # Ask the user about which dog breed
                dog_input = input("Which dog breed would you like more information about (must match exactly)? ")

                # Find the dogs record in the previous list
                search_list = [dog for dog in dogs if dog["name"] == dog_input]
                found_dog = None if len(search_list) != 1 else search_list[0]

                if not found_dog:
                    # Ask the user to enter a valid input
                    print(f"The dog breed entered, '{dog_input}', was not on the previous list. Please try again.\n")
                else:
                    # Break out of this while loop
                    break

            # Print the name of the dog before the rest of the info
            print(f"\nName: {found_dog['name']}")

            # Go through each item in the dictionary
            for key, value in found_dog.items():

                # Print every item that is not the name
                if key != "name":
                    print(f"{str(key).capitalize().replace('_', ' ')}: {value}")

            # Extra print for formatting after the list of items
            print()

        # If there was offset, meaning we are on the next page of the list
        if offset:
            # Ask the user if they would like to see the previous page
            back_input = input("Would you like like to go back to the previous results? ")

            # If they agree
            if back_input in ("yes", "y", "1"):

                # Decrease the offset by 20 to get the previous 20 in the API
                offset -= 20

                # Set back to True to avoid asking the criteria questions
                back = True

                # Continue to the next iteration of the loop
                continue
            else:
                # Ensure that back is equal to False
                back = False

        # If the API response max was returned, see if they want to go to the next 20 dogs
        if len(dogs) == 20:

            # Explain the max of 20 dogs per call
            offset_input = input(
                "There is a maximum of 20 names per list. "
                "Would you like the next list of names for the same criteria? "
            )

            # Check if the user agreed
            if offset_input in ("yes", "y", "1"):

                # Increase the offset by 20 to get the next 20 in the API
                offset += 20

                # Continue to the next iteration of the loop
                continue
            else:
                # Reset the offset variable if the user is not going back or forward with this search
                offset = 0

        # Check if the user would like to stop the program
        more_input = input("Would you like more dog breeds? ")
        if more_input not in ("yes", "y", "1"):

            # Break out of the infinite while loop
            break

        # Extra line for formatting
        print()

    # Print a final message to the user
    print("\nHave a great day!")


if __name__ == "__main__":
    # Run the main function
    main()
