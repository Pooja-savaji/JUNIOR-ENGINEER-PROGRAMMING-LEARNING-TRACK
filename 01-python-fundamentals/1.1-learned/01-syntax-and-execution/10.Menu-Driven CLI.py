print("1. Add")
print("2. Subtract")
choice = int(input("Enter choice: "))
a = float(input("Enter first number: "))
b = float(input("Enter second number: "))
if choice == 1:
    print("Result:", a + b)
elif choice == 2:
    print("Result:", a - b)
else:
    print("Invalid choice")
