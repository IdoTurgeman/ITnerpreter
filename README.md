# Ithon Interpreter

Ithon is a simple interpreter for a custom programming language, written in Python. The interpreter can execute source code files containing variable declarations, expressions, print statements, and basic operations. 

## Features

- Variable declaration and assignment
- Arithmetic and logical expressions
- Print statements

## Installation

### 1. Clone the repository

Clone the Ithon interpreter repository from GitHub:
```bash
git clone https://github.com/IdoTurgeman/Ithon.git
```

### 2. Make the script executable:
```bash
cd Ithon
chmod +x Ithon.py
```

### 3. Create a symbolic link:

```bash
ln -s $(pwd)/Ithon.py /usr/local/bin/Ithon
```

## Usage
Run the interpreter with:
```bash
Ithon <filename> [optional command]
  - commands:[tokenize, parse, execute: default]
```

## Example
Example code in test.it:
```text
var a = 5
var b = 10

var result = a + b * 2
print("result")
print(result)
```

Run it with:
```bash
Ithon test.it
```

