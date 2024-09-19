from flask import Flask

app = Flask(__name__)

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# Create routes for each operation
@app.route('/')
def home():
    return "Welcome to the Calculator API!"

@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    calc = Calculator()
    result = calc.add(a, b)
    return f"Addition: {result}"

@app.route('/subtract/<int:a>/<int:b>')
def subtract(a, b):
    calc = Calculator()
    result = calc.subtract(a, b)
    return f"Subtraction: {result}"

@app.route('/multiply/<int:a>/<int:b>')
def multiply(a, b):
    calc = Calculator()
    result = calc.multiply(a, b)
    return f"Multiplication: {result}"

@app.route('/divide/<int:a>/<int:b>')
def divide(a, b):
    calc = Calculator()
    result = calc.divide(a, b)
    return f"Division: {result}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
