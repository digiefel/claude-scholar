# Python Error Reference

## Common Built-in Exception Types

### 1. SyntaxError

**Characteristic**: Code cannot be parsed; detected before execution

**Common causes**:
- Mismatched parentheses
- Missing colon
- Incorrect indentation
- Mismatched quotes

**Example**:
```python
# Missing colon
if True
    print("missing colon")

# Correct
if True:
    print("has colon")
```

### 2. IndentationError

**Characteristic**: Inconsistent indentation or wrong indentation type

**Common causes**:
- Mixing tabs and spaces
- Wrong indentation level

**Example**:
```python
# Mixing spaces and tabs
def test():
	    print("mixed")  # tab
    print("spaces")    # spaces

# Correct: use 4 spaces consistently
def test():
    print("spaces")
    print("consistent")
```

### 3. NameError

**Characteristic**: Variable or function name does not exist

**Common causes**:
- Using a variable before defining it
- Misspelled function name
- Variable scope issue

**Example**:
```python
# Variable not defined
print(undefined_var)

# Correct: define before use
my_var = 42
print(my_var)
```

### 4. TypeError

**Characteristic**: Operation or function applied to wrong data type

**Common causes**:
- Concatenating incompatible types
- Wrong argument type for function
- Using operator on unsupported types

**Example**:
```python
# Concatenating string and number
result = "Value: " + 42

# Correct: convert type
result = "Value: " + str(42)
# Or use f-string
result = f"Value: {42}"
```

### 5. AttributeError

**Characteristic**: Object does not have the specified attribute or method

**Common causes**:
- Misspelled attribute name
- Object is not the expected type
- Wrong capitalization

**Example**:
```python
# List has no push method
my_list = [1, 2, 3]
my_list.push(4)  # list has no push method

# Correct: use the right method
my_list.append(4)
```

### 6. KeyError

**Characteristic**: Specified key does not exist in dictionary

**Common causes**:
- Misspelled key name
- Key does not exist in dictionary

**Example**:
```python
data = {"name": "Alice"}

# Directly accessing non-existent key
age = data["age"]  # KeyError

# Correct: use get() method
age = data.get("age", 0)  # returns default value 0
```

### 7. IndexError

**Characteristic**: Sequence index out of range

**Common causes**:
- Negative index (unless intentional)
- Index greater than sequence length minus 1
- Accessing index on empty sequence

**Example**:
```python
items = [1, 2, 3]

# Index out of range
item = items[5]  # IndexError

# Correct: check length before accessing
if len(items) > 5:
    item = items[5]
else:
    item = None
```

### 8. ValueError

**Characteristic**: Argument type is correct but value is inappropriate

**Common causes**:
- String to integer conversion fails
- Math operation value out of domain
- Argument value outside allowed range

**Example**:
```python
# Cannot convert to integer
num = int("abc")

# Correct: handle possible error
try:
    num = int(input())
except ValueError:
    num = 0
```

### 9. ImportError / ModuleNotFoundError

**Characteristic**: Cannot import module

**Common causes**:
- Module not installed
- Module path not in PYTHONPATH
- Misspelled module name

**Example**:
```python
# Module not installed
import missing_module

# Solution: install the module
# pip install missing-module
```

### 10. FileNotFoundError

**Characteristic**: Attempting to open a file that does not exist

**Common causes**:
- Wrong file path
- File does not exist
- Incorrect relative path usage

**Example**:
```python
# File does not exist
with open("missing.txt") as f:
    content = f.read()

# Correct: use try-except or check existence
try:
    with open("file.txt") as f:
        content = f.read()
except FileNotFoundError:
    content = ""
```

## Exception Handling Best Practices

### 1. Catch specific exceptions

```python
# Catch all exceptions (bad practice)
try:
    result = dangerous_operation()
except:
    pass

# Correct: catch specific exceptions
try:
    result = dangerous_operation()
except (ValueError, TypeError) as e:
    logger.error(f"Operation failed: {e}")
```

### 2. Use finally to clean up resources

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    content = ""
finally:
    # Executes regardless of whether an exception occurred
    if 'file' in locals():
        file.close()
```

### 3. Use context managers

```python
# Recommended: use with statement
with open("data.txt", "r") as file:
    content = file.read()
# File is automatically closed
```

### 4. Chained exceptions

```python
try:
    process_data(data)
except ValueError as e:
    # Use raise from to preserve original exception
    raise RuntimeError("Data processing failed") from e
```

## Debugging Techniques

### 1. Use the traceback module

```python
import traceback

try:
    risky_operation()
except Exception:
    # Print full stack trace
    traceback.print_exc()
```

### 2. Use the pdb debugger

```python
import pdb

# Set a breakpoint in code
pdb.set_trace()

# Or use breakpoint() (Python 3.7+)
breakpoint()
```

### 3. Use the logging module

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug information")
logger.info("General information")
logger.warning("Warning")
logger.error("Error")
logger.critical("Critical error")
```

## Common Error Troubleshooting Checklist

- [ ] Check spelling (variable names, function names, attribute names)
- [ ] Check data types (use type() function)
- [ ] Check variable values (use print() or debugger)
- [ ] Check that indexes and keys are within range
- [ ] Check that file paths are correct
- [ ] Check that indentation is consistent
- [ ] Check that parentheses and quotes are matched
- [ ] Check that modules are correctly imported
- [ ] Check that exceptions are properly handled
