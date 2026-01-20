def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    while True:
        print("\nSimple Calculator")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")
        choice = input("Choose operation (1-5): ")
        
        if choice == '5':
            print("Exiting calculator.")
            break
        
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numbers.")
            continue
        
        if choice == '1':
            result = add(a, b)
            print(f"Result: {a} + {b} = {result}")
        elif choice == '2':
            result = subtract(a, b)
            print(f"Result: {a} - {b} = {result}")
        elif choice == '3':
            result = multiply(a, b)
            print(f"Result: {a} * {b} = {result}")
        elif choice == '4':
            try:
                result = divide(a, b)
                print(f"Result: {a} / {b} = {result}")
            except ValueError as e:
                print(e)
        else:
            print("Invalid choice. Please select 1-5.")