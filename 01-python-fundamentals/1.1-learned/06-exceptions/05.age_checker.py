
def check_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative.")

    if age > 120:
        raise ValueError("Age is not valid.")

    return True


try:
    age = int(input("Enter your age: "))

    if check_age(age):
        print("Age is valid.")

except ValueError as error:
    print("Error:", error)
