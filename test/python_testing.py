file_name = input("Enter the desired file name: ")
file = open(file_name, 'w') # with open
content = input("Enter the content to be written to the file: ")
file.write(content)
file.close()
print("File saved successfully!")