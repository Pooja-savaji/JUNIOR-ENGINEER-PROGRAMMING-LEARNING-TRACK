while True:
    print("\n1. Add")
    print("2. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        a = int(input("Enter number: "))
        b = int(input("Enter number: "))
        print("Result:", a + b)

    elif choice == 2:
        print("Goodbye!")
        break

    else:
        print("Invalid choice")
