"""
Debugging workflow example

This example demonstrates a complete debugging workflow,
from identifying a problem to resolving it.
"""

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================
# Problem 1: IndexError
# ============================================

def get_item(items, index):
    """
    Problem: Directly accessing an index may cause IndexError

    Error symptom:
    IndexError: list index out of range
    """
    # Problematic code
    # return items[index]

    # Fixed code
    if 0 <= index < len(items):
        return items[index]
    else:
        logger.warning(f"Index {index} out of range [0, {len(items)})")
        return None


# ============================================
# Problem 2: TypeError - string concatenation
# ============================================

def format_message(name, count):
    """
    Problem: Attempting to concatenate a string and a number

    Error symptom:
    TypeError: can only concatenate str (not "int") to str
    """
    # Problematic code
    # return name + ": " + count

    # Fixed code
    return f"{name}: {count}"
    # Or
    # return name + ": " + str(count)


# ============================================
# Problem 3: KeyError
# ============================================

def get_user_info(users, user_id):
    """
    Problem: Directly accessing a key that may not exist in the dictionary

    Error symptom:
    KeyError: 'user_123'
    """
    # Problematic code
    # return users[user_id]

    # Fixed code option 1: use get()
    return users.get(user_id, None)

    # Fixed code option 2: check if key exists
    # if user_id in users:
    #     return users[user_id]
    # return None


# ============================================
# Problem 4: AttributeError - None object
# ============================================

def process_data(data_provider):
    """
    Problem: data_provider may return None

    Error symptom:
    AttributeError: 'NoneType' object has no attribute 'process'
    """
    data = data_provider.get_data()

    # Problematic code
    # return data.process()

    # Fixed code
    if data is not None:
        return data.process()
    else:
        logger.error("Data is None, cannot process")
        return None


# ============================================
# Problem 5: Modifying list while iterating
# ============================================

def remove_even_numbers(numbers):
    """
    Problem: Modifying list during iteration causes elements to be skipped

    Error symptom:
    Some even numbers are not removed
    """
    # Problematic code
    # for num in numbers:
    #     if num % 2 == 0:
    #         numbers.remove(num)
    # return numbers

    # Fixed code option 1: list comprehension
    return [num for num in numbers if num % 2 != 0]

    # Fixed code option 2: use a copy
    # for num in numbers[:]:
    #     if num % 2 == 0:
    #         numbers.remove(num)
    # return numbers


# ============================================
# Debugging technique example
# ============================================

def debug_with_logging(data):
    """
    Use logging to trace the problem
    """
    logger.debug(f"Input data: {data}")

    # Step 1
    processed = step1(data)
    logger.debug(f"Step 1 result: {processed}")

    # Step 2
    result = step2(processed)
    logger.debug(f"Step 2 result: {result}")

    return result


def step1(data):
    """Simulate step 1"""
    return [x * 2 for x in data]


def step2(data):
    """Simulate step 2"""
    return sum(data)


# ============================================
# Exception handling example
# ============================================

def safe_divide(a, b):
    """
    Correct exception handling pattern
    """
    try:
        result = a / b
        logger.info(f"{a} / {b} = {result}")
        return result
    except ZeroDivisionError:
        logger.error(f"Divisor cannot be zero: {b}")
        return None
    except TypeError as e:
        logger.error(f"Type error: {e}")
        return None


# ============================================
# Using assertions for debugging
# ============================================

def calculate_discount(price, discount_rate):
    """
    Use assertions to verify assumptions
    """
    # Assert: price should be positive
    assert price > 0, f"Price should be positive, got: {price}"

    # Assert: discount rate should be between 0 and 1
    assert 0 <= discount_rate <= 1, f"Discount rate should be between 0 and 1, got: {discount_rate}"

    discounted_price = price * (1 - discount_rate)

    # Assert: discounted price should be less than original
    assert discounted_price <= price, "Discounted price should be less than original"

    return discounted_price


# ============================================
# Test code
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("Debugging Examples")
    print("=" * 50)

    # Test get_item
    print("\n1. Test get_item:")
    items = ['a', 'b', 'c']
    print(f"get_item(items, 1) = {get_item(items, 1)}")
    print(f"get_item(items, 10) = {get_item(items, 10)}")

    # Test format_message
    print("\n2. Test format_message:")
    print(f"format_message('Count', 42) = {format_message('Count', 42)}")

    # Test get_user_info
    print("\n3. Test get_user_info:")
    users = {'user_1': 'Alice', 'user_2': 'Bob'}
    print(f"get_user_info(users, 'user_1') = {get_user_info(users, 'user_1')}")
    print(f"get_user_info(users, 'user_999') = {get_user_info(users, 'user_999')}")

    # Test remove_even_numbers
    print("\n4. Test remove_even_numbers:")
    numbers = [1, 2, 3, 4, 5, 6]
    print(f"Original: {numbers}")
    print(f"Result: {remove_even_numbers(numbers)}")

    # Test safe_divide
    print("\n5. Test safe_divide:")
    print(f"safe_divide(10, 2) = {safe_divide(10, 2)}")
    print(f"safe_divide(10, 0) = {safe_divide(10, 0)}")

    # Test calculate_discount
    print("\n6. Test calculate_discount:")
    print(f"calculate_discount(100, 0.2) = {calculate_discount(100, 0.2)}")
