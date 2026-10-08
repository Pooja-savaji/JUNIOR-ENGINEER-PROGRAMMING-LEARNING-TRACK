
# Exercise 1
# Error: ZeroDivisionError
# Reason: Cannot divide a number by zero.
print(10 / 0)

# Exercise 2
# Error: IndexError
# Reason: Index 10 does not exist in the string.
name = "Pooja"
print(name[10])

# Exercise 3
# Error: TypeError
# Reason: Cannot add an integer to a string.
age = "20"
print(age + 5)

# Exercise 4
# Error: IndexError
# Reason: List has only indexes 0, 1, and 2.
numbers = [1, 2, 3]
print(numbers[5])

# Exercise 5
# Error: KeyError
# Reason: "email" key does not exist in the dictionary.
user = {"name": "Pooja"}
print(user["email"])

# Exercise 6
# Error: TypeError
# Reason: List indexes must be integers, not strings.
numbers = [1, 2, 3]
print(numbers["0"])

# Exercise 7
# Error: NameError
# Reason: Variable "message" is not defined.
def exercise_7():
    print(message)
exercise_7()

# Exercise 8
# Error: TypeError
# Reason: Function needs two arguments, but only one is given.
def add(a, b):
    return a + b
print(add(10))

# Exercise 9
# Error: TypeError
# Reason: sum() accepts at most two arguments.
numbers = [1, 2, 3]
print(sum(numbers, 10, 20))

# Exercise 10
# Error: AttributeError
# Reason: Strings do not have an "uppercase()" method.
text = "hello"
print(text.uppercase())

# Exercise 11
# Error: TypeError
# Reason: None cannot be accessed like a dictionary.
user = None
print(user["name"])

# Exercise 12
# Error: ZeroDivisionError
# Reason: Cannot divide by zero.
numbers = [10, 20, 30]
total = sum(numbers)
print(total / 0)

# Exercise 13
# Error: ZeroDivisionError
# Reason: len(numbers) is 0, so division by zero happens.
numbers = []
print(sum(numbers) / len(numbers))

# Exercise 14
# Error: TypeError
# Reason: None has no length.
data = None
print(len(data))

# Exercise 15
# Error: TypeError
# Reason: Cannot add an integer and a string.
price = 100
quantity = "2"
print(price + quantity)
