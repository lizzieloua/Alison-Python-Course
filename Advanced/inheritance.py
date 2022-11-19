# Import the required libraries
import sys


class Animal:
    # An animal's name
    name = ""

    # An animal's age
    age = 0

    def __init__(
        self,
        *,
        name: str,
        age: int,
    ):

        # Display a message to track code progress
        print("Creating a new animal!")

        # Set up the object variables using the information given
        self.name = name.capitalize()
        self.age = age

    def __str__(self) -> str:
        """ Override the string function to format it appropriately """
        return (
                "\n------------ Animal Information ------------\n" +
                f"Name: {self.name}\n" +
                f"Age: {self.age}\n"
        )

    def __repr__(self) -> str:
        """ Override the internal representation to use our overriden str message """
        return str(self)

    def __eq__(self, target) -> bool:
        """ Override the equal to compare our overriden str message """
        return str(self) == str(target)

    def speak(self) -> None:
        """ This function displays a message from the animal """
        print(f"{self.name}: I'm speaking!")

    def move(self) -> None:
        """ This function displays a message from the animal """
        print(f"{self.name}: I'm moving!")

    def eat(self) -> None:
        """ This function displays a message from the animal """
        print(f"{self.name}: Nom Nom Nom!")


class Dog(Animal):

    def __init__(
            self,
            *,
            name: str,
            age: int,
    ):
        super().__init__(name=name, age=age)
        self.breed = "German Shepard"

    def __str__(self) -> str:
        """ Override the string function to format it appropriately """
        return (
                "\n------------ Dog Information ------------\n" +
                f"Name: {self.name}\n" +
                f"Breed: {self.breed}\n" +
                f"Age: {self.age}\n"

        )

    def speak(self) -> None:
        """ This function displays a message from the animal """
        print(f"{self.name}: Woof Woof!")

    def move(self) -> None:
        """ This function displays a message from the animal """
        print(f"{self.name}: I'm running!")


def main():
    # args is a list of the command line arguments, starts at index 1 because index 0 is the file name
    args = sys.argv[1:]

    # We expect 4 arguments, raise an exception if not provided
    if len(args) != 2:
        raise Exception(
            "This program expects 2 arguments.\n"
            "Please try re-running the program and provide name and age."
        )

    # Create a variable using the custom object, Animal
    animal = Animal(name=args[0], age=int(args[1]))

    # Display the animal's initial information
    print(animal)

    # Display the animal speaking, moving, and eating
    animal.speak()
    animal.move()
    animal.eat()

    print("<-------------------- Switching Classes -------------------->")

    # Create a variable using the custom object, Dog
    dog = Dog(name=args[0], age=int(args[1]))

    # Display the dog's initial information
    print(dog)

    # Display the dog speaking, moving, and eating
    dog.speak()
    dog.move()
    dog.eat()


if __name__ == "__main__":
    main()
