x = 50
y = 20.5
x = "Hello"
x = [1, 2, 3, 4, 5]
x = ("a", "b", "c")
x = {"name": "Alice", "age": 30}

# Numeric Data Types
a = 10  # This is an integer
b = 3.14  # This is a floating-point number
c = 2 + 3j  # This is a complex number

print(type(a))
print(type(b))
print(type(c))

# String Data Type
name = "Aswin"
greeting = 'Hello, World!'
print(type(name))
print(type(greeting))

# accessing characters in a string
print(name[0])  # Output: 'A'
print(greeting[0])  # Output: 'H'   


# List Data Type
my_list = [1, 2, 3, 4, 5]
print(type(my_list))
print(my_list[0])  # Output: 1

# Tuple Data Type
my_tuple = ("a", "b", "c")
print(type(my_tuple))
print(my_tuple[0])  # Output: 'a'

# Dictionary Data Type
my_dict = {"name": "Alice", "age": 30}
print(type(my_dict))
print(my_dict["name"])  # Output: 'Alice'

# Boolean Data Type
is_valid = True
is_expired = False
print(type(is_valid))
print(type(is_expired))

# None Data Type
result = None
print(type(result))
print(result)  # Output: None

# Truth and Falsy Values
if 1:
    print("1 is truthy")
if 0:
    print("0 is falsy")

# Set Data Type
s1 = {"apple", "banana", "cherry"}
for i in s1:
    print(i)

# Frozen Set Data Type
s2 = frozenset({"apple", "banana", "cherry"})
for i in s2:
    print(i)

# Dictionary Data Type
my_dict = {"name": "Alice", "age": 30}
print(my_dict["name"])  # Output: 'Alice'
print(my_dict["age"])   # Output: 30
print(my_dict.get("name"))  # Output: 'Alice'
print(my_dict.get("age"))   # Output: 30
