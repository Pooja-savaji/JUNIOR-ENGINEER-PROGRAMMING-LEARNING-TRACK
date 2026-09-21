
def validate_number(number):
    if number <= 0:
        raise ValueError("Number must be greater than zero.")

    return True


try:
    number = int(input("Enter a positive number: "))
    validate_number(number)
    print("Number is valid.")

except ValueError as error:
    print("Error:", error)
