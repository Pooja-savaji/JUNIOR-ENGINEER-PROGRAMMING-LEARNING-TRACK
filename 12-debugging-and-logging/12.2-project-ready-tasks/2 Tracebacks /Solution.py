# 15.2 Tracebacks - Solutions

# Solution 1
print(10 / 2)

# Solution 2
name = "Pooja"
print(name[0])

# Solution 3
age = "20"
print(int(age) + 5)

# Solution 4
numbers = [1, 2, 3]
print(numbers[2])

# Solution 5
user = {"name": "Pooja"}
print(user["name"])

# Solution 6
numbers = [1, 2, 3]
print(numbers[0])

# Solution 7
def greet():
    message = "Hello"
    print(message)
greet()

# Solution 8
def add(a, b):
    return a + b
print(add(10, 5))

# Solution 9
numbers = [1, 2, 3]
print(sum(numbers))

# Solution 10
text = "hello"
print(text.upper())

# Solution 11
def get_name(user):
    return user["name"]
print(get_name({"name": "Pooja"}))

# Solution 12
numbers = [10, 20, 30]
total = sum(numbers)
print(total / 2)

# Solution 13
def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
numbers = []
print(average(numbers))

# Solution 14
data = []
print(len(data))

# Solution 15
def calculate(price, quantity):
    return price * quantity
price = 100
quantity = 2
print(calculate(price, quantity))
