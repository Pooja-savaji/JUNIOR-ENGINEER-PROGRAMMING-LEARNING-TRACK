
try:
    number = int(input("Enter a number: "))
    result = 20 / number

except ValueError:
    print("Invalid input.")

except ZeroDivisionError:
    print("Cannot divide by zero.")

else:
    print("Result:", result)

finally:
    print("Program completed.")
