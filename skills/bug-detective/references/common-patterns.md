# Common Error Patterns

## General Programming Error Patterns

### 1. Off-by-one Error

**Description**: A ±1 discrepancy in loops or indexes

**Example**:
```python
# Wrong: range should be range(n) not range(n+1)
for i in range(len(items) + 1):
    print(items[i])  # IndexError

# Correct
for i in range(len(items)):
    print(items[i])
```

### 2. Null/None Reference Error

**Description**: Attempting to access attributes or methods on a None object

**Python**:
```python
# May return None
result = get_data()
print(result.value)  # AttributeError

# Correct: check for None
result = get_data()
if result is not None:
    print(result.value)
```

**JavaScript**:
```javascript
// May be null
const user = getUser();
console.log(user.name);  // TypeError

// Correct: use optional chaining
console.log(user?.name);
```

### 3. Resource Leak

**Description**: Opened resources (files, connections) not properly closed

**Python**:
```python
# File may not be closed
f = open("file.txt")
content = f.read()
# If an exception occurs, file will not be closed

# Correct: use with statement
with open("file.txt") as f:
    content = f.read()
# File is automatically closed
```

### 4. Race Condition

**Description**: Timing dependency issue between multiple threads/processes

**Example**:
```python
# Check-then-use (TOCTOU)
if os.path.exists("file.txt"):
    # Another process may delete the file in between
    with open("file.txt") as f:
        content = f.read()

# Correct: try directly and handle exception
try:
    with open("file.txt") as f:
        content = f.read()
except FileNotFoundError:
    content = None
```

### 5. Forgetting Return Value

**Description**: Function has no explicit return value, resulting in returning None

**Example**:
```python
# Forgot to return result
def calculate(x, y):
    result = x + y
    # forgot return

# Correct: return explicitly
def calculate(x, y):
    return x + y
```

### 6. Wrong Comparison Operator

**Description**: Using = instead of ==, or confusing is with ==

**Python**:
```python
# Assignment instead of comparison
if x = 5:  # SyntaxError

# Using is for value comparison
if x is 5:  # not guaranteed to be correct

# Correct
if x == 5:
```

### 7. Floating-Point Precision Issues

**Description**: Floating-point comparison fails due to precision

**Example**:
```python
# Direct float comparison
if 0.1 + 0.2 == 0.3:  # False
    print("equal")

# Correct: use tolerance comparison
if abs((0.1 + 0.2) - 0.3) < 1e-9:
    print("equal")

# Or use math.isclose()
import math
if math.isclose(0.1 + 0.2, 0.3):
    print("equal")
```

### 8. String Concatenation Performance

**Description**: Using + to concatenate strings inside a loop

**Example**:
```python
# Inefficient: creates new string each time
result = ""
for item in items:
    result += str(item)

# Efficient: use list and join
result = "".join(str(item) for item in items)
```

## Python-Specific Patterns

### 1. Mutable Default Arguments

```python
# All calls share the same list
def append(item, items=[]):
    items.append(item)
    return items

# Correct: use None as default value
def append(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 2. Closure Variable Binding

```python
# All functions use the same i value
funcs = [lambda: i for i in range(3)]
# All functions return 2

# Correct: capture value using default argument
funcs = [lambda i=i: i for i in range(3)]
```

### 3. Modifying a Sequence While Iterating

```python
# Modifying list while iterating causes skipped elements
items = [1, 2, 3, 4]
for item in items:
    if item % 2 == 0:
        items.remove(item)

# Correct option 1: list comprehension
items = [item for item in items if item % 2 != 0]

# Correct option 2: iterate over a copy
for item in items[:]:
    if item % 2 == 0:
        items.remove(item)
```

## JavaScript/TypeScript-Specific Patterns

### 1. this Binding Issues

```javascript
// this loses context
class Counter {
  count = 0;
  increment() {
    setTimeout(function() {
      this.count++;  // this is not the Counter instance
    }, 100);
  }
}

// Correct: use arrow function
class Counter {
  count = 0;
  increment() {
    setTimeout(() => {
      this.count++;  // this is correctly bound
    }, 100);
  }
}
```

### 2. Async Error Handling

```javascript
// Promise error not handled
async function getData() {
  const response = await fetch(url);
  return response.json();  // throws if it fails
}

// Correct: use try-catch
async function getData() {
  try {
    const response = await fetch(url);
    return await response.json();
  } catch (error) {
    console.error("Failed to fetch data:", error);
    throw error;
  }
}
```

### 3. Array/Object References

```javascript
// Direct assignment copies the reference
const arr1 = [1, 2, 3];
const arr2 = arr1;
arr2.push(4);  // arr1 is also modified

// Correct: create a copy
const arr2 = [...arr1];  // or arr1.slice()

// Objects
const obj1 = { a: 1 };
const obj2 = { ...obj1 };  // or Object.assign({}, obj1)
```

## Concurrency Error Patterns

### 1. Deadlock

```python
# May deadlock
import threading

lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1():
    with lock1:
        with lock2:
            # operation

def thread2():
    with lock2:
        with lock1:  # deadlock
            # operation
```

### 2. Data Race

```python
# Multiple threads simultaneously modifying shared variable
counter = 0

def increment():
    global counter
    counter += 1  # non-atomic operation

# Correct: use a lock
counter = 0
lock = threading.Lock()

def increment():
    global counter
    with lock:
        counter += 1
```

## Prevention Measures

1. **Use type checking**: TypeScript, Python type annotations
2. **Write unit tests**: cover boundary conditions
3. **Use static analysis tools**: pylint, eslint
4. **Code review**: have others check the code
5. **Use defensive programming**: validate inputs, handle exceptions
