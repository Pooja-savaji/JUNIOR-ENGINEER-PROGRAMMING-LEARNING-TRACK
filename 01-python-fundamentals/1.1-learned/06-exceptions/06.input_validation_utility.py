
def get_positive_number():
    while True:
        try:
            number = int(input("Enter a positive number: "))

            if number <= 0:
                raise ValueError("Number must be positive.")

            return number

        except ValueError as error:
            print("Error:", error)


number = get_positive_number()
print("Valid number:", number)
