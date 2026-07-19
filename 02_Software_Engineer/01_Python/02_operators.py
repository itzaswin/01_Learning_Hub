a = 15
b = 4


# Arithmetic Operators
## These operators perform basic mathematical operations on numbers.

print("Addition:", a + b)  

print("Subtraction:", a - b) 

print("Multiplication:", a * b)  

print("Division:", a / b) 

# Floor Division gives the quotient without the remainder 
# Example 16 // 4 = 4 (because 4 goes into 16 four times with no remainder)
print("Floor Division:", a // b)  

# Modulus gives the remainder of the division
# Example 16 % 4 = 0 (because when you divide 16 by 4, the remainder is 0)
print("Modulus:", a % b) 

# Exponentiation raises the first number to the power of the second number
# Example  2 ** 3 = 8 (because 2 multiplied by itself 3 times is 8)
print("Exponentiation:", a**b)


# Comparison Operators
## These operators compare two values and return a boolean result (True or False).

print("Equal to:", a == b)
print("Not Equal to:", a != b)
print("Greater than:", a > b)
print("Less than:", a < b)
print("Greater than or Equal to:", a >= b)
print("Less than or Equal to:", a <= b)


# Logical Operators
## These operators are used to combine conditional statements.
# The 'and' operator returns True if both conditions are true, otherwise it returns False.
# The 'or' operator returns True if at least one of the conditions is true, otherwise
# it returns False.
# The 'not' operator returns the opposite of the condition. If the condition is true,
# it returns False, and if the condition is false, it returns True.

x = True
y = False

print("AND:", x and y)
print("OR:", x or y)
print("NOT:", not x)


# Assignment Operators
## These operators are used to assign values to variables. They can also perform an operation
# and assign the result to the variable in one step.

c = 10
c += 5  # This is equivalent to c = c + 5
print("After += 5:", c)

c -= 3  # This is equivalent to c = c - 3
print("After -= 3:", c)

c *= 2  # This is equivalent to c = c * 2
print("After *= 2:", c)

c /= 4  # This is equivalent to c = c / 4
print("After /= 4:", c)

c //= 2  # This is equivalent to c = c // 2
print("After //= 2:", c)

c %= 3  # This is equivalent to c = c % 3
print("After %= 3:", c)

# Membership Operators
## These operators are used to test if a value is present in a sequence (like a list
# or a string).

my_list = [1, 2, 3, 4, 5]
print("Is 3 in the list?", 3 in my_list)
print("Is 6 in the list?", 6 in my_list)

my_string = "Hello, World!"
print("Is 'Hello' in the string?", "Hello" in my_string)
print("Is 'Python' in the string?", "Python" in my_string)


# Identity Operators
## These operators are used to compare the memory locations of two objects. The 'is' operator
# returns True if both operands refer to the same object, while the 'is not' operator returns
# True if they refer to different objects.

a = [1, 2, 3]
b = a  # b refers to the same list as a
c = [1, 2, 3]  # c is a different list with
# the same content as a and b
print("a is b:", a is b)  # True, because a and b refer to the same object
print("a is c:", a is c)  # False, because a and c refer to different objects   
print("a is not c:", a is not c)  # True, because a and c refer to different objects


# Ternary Operator
## This operator is a shorthand for an if-else statement. It allows you to assign a
# value to a variable based on a condition in a single line of code.

age = 20
status = "Adult" if age >= 18 else "Minor"
print("Status:", status)

# Bitwise Operators
## These operators perform bit-level operations on integers. They include AND (&), OR (|),
# XOR (^), NOT (~), left shift (<<), and right shift (>>).

x = 5  # In binary: 0101
y = 3  # In binary: 0011
print("Bitwise AND:", x & y)  # 1 (In binary: 0001)
print("Bitwise OR:", x | y)   # 7 (In binary: 0111)
print("Bitwise XOR:", x ^ y)  # 6 (In binary: 0110)
print("Bitwise NOT:", ~x)     # -6 (In binary: 1010, which is the two's complement of 5)
print("Left Shift:", x << 1)  # 10 (In binary: 1010)
print("Right Shift:", x >> 1) # 2 (In binary: 0010) 

# Procedence and Associativity of Operators
## Operator precedence determines the order in which operators are evaluated in an expression.
## Associativity determines the order in which operators of the same precedence are evaluated.
## For example, in the expression 3 + 4 * 2, the multiplication operator

expr = 3 + 4 * 2
print("Result of 3 + 4 * 2:", expr)  # Output: 11, because multiplication has higher precedence than addition

name = "Aswin"
greeting = "Hello, " + name + "!"
print(greeting)  # Output: Hello, Aswin!    

if name == "Aswin" and greeting == "Hello, Aswin!":
    print("Welcome, Aswin!")
else:
    print("Welcome, Guest!")

# Operator Associativity Example

result = 10 - 5 + 2
print("Result of 10 - 5 + 2:", result)  # Output: 7, because both subtraction and addition have the same precedence and are evaluated from left to right (associativity)
print(100 / 10 * 10)
print(5 - 2 + 3)
print(5 - (2 + 3))
print(2 ** 3 ** 2)