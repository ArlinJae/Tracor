# Starting the script execution
print("Script execution started...")

# Variable assignments
x = 42
y = 0

# Correct arithmetic operation
result = x + 8
print(f"Result of x + 8 is: {result}")

# Function definition and invocation
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")

# Deliberate division by zero error
try:
    result = x / y
except ZeroDivisionError:
    print("Handled division by zero error.")

# Loop with a correct operation
for i in range(5):
    print(f"Loop iteration {i}")

# Multiline statement
total = (x +
         10 +
         5)
print(f"Total value is: {total}")

# Deliberate NameError
print(f"Undefined variable: {undefined_variable}")

# Function with an error
def calculate_area(radius):
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    return 3.14 * radius ** 2

# Correct function call
area = calculate_area(5)
print(f"Area of circle with radius 5: {area}")

# Deliberate ValueError
try:
    area = calculate_area(-3)
except ValueError as e:
    print(f"Handled error: {e}")

# Another deliberate error: TypeError
try:
    area = calculate_area("radius")
except TypeError as e:
    print(f"Handled error: {e}")

# A correct loop
for i in range(3):
    print(f"Second loop iteration {i}")

# Deliberate IndexError
my_list = [1, 2, 3]
try:
    print(my_list[5])
except IndexError as e:
    print(f"Handled error: {e}")

# End of script
print("Script execution finished.")
