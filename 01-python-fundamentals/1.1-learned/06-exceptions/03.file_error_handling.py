
try:
    file = open("data.txt", "r")
    content = file.read()
    print(content)
    file.close()

except FileNotFoundError:
    print("File was not found.")
