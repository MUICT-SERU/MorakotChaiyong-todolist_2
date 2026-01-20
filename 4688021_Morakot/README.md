# Simple Calculator

A simple command-line calculator that supports addition, subtraction, multiplication, and division.

## Features

- Add two numbers
- Subtract two numbers
- Multiply two numbers
- Divide two numbers (with division by zero protection)
- Interactive command-line interface

## Usage

Run the calculator:

```bash
python calculator.py
```

Follow the prompts to select an operation and enter numbers.

## Testing

Run the tests:

```bash
pytest test_calculator.py
```

Or with coverage:

```bash
pytest --cov=calculator test_calculator.py
```

## Requirements

- Python 3.6+
- pytest (for testing)