"""
Error handling pattern examples

Demonstrates best practices for various error handling scenarios.
"""

import logging
from typing import Optional, List, Dict, Any
from functools import wraps

logger = logging.getLogger(__name__)


# ============================================
# Pattern 1: Catch specific exceptions
# ============================================

def read_file(filepath: str) -> Optional[str]:
    """
    Catch specific exceptions rather than a broad Exception
    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return None
    except PermissionError:
        logger.error(f"No permission to read file: {filepath}")
        return None
    except UnicodeDecodeError:
        logger.error(f"File encoding error: {filepath}")
        return None


# ============================================
# Pattern 2: Operation with retry
# ============================================

def retry_operation(max_attempts: int = 3):
    """
    Decorator: automatically retry failed operations
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        logger.error(f"Operation failed after {max_attempts} attempts: {e}")
                        raise
                    logger.warning(f"Operation failed, retrying (attempt {attempt})...")
            return None
        return wrapper
    return decorator


@retry_operation(max_attempts=3)
def unstable_api_call() -> Dict[str, Any]:
    """
    Simulate an unstable API call
    """
    import random
    if random.random() < 0.7:  # 70% failure rate
        raise ConnectionError("API connection failed")
    return {"status": "success", "data": "result"}


# ============================================
# Pattern 3: Context manager for resource handling
# ============================================

class DatabaseConnection:
    """
    Custom context manager to ensure resources are properly released
    """
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    def __enter__(self):
        logger.info(f"Connecting to database: {self.connection_string}")
        self.connection = f"Connection to {self.connection_string}"
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.error(f"Exception occurred: {exc_val}")
        logger.info("Closing database connection")
        # Clean up resources
        self.connection = None
        return False  # Do not suppress the exception


# ============================================
# Pattern 4: Chained exceptions (preserve original exception)
# ============================================

def validate_and_process(data: Dict[str, Any]) -> Any:
    """
    Use raise from to preserve the original exception chain
    """
    try:
        # Validate data
        if 'value' not in data:
            raise ValueError("Missing 'value' field in data")

        value = data['value']
        if not isinstance(value, (int, float)):
            raise TypeError(f"value should be a number, got type: {type(value)}")

        # Process data
        return value * 2

    except (ValueError, TypeError) as e:
        # Preserve original exception and add context
        raise RuntimeError(f"Data processing failed: {data}") from e


# ============================================
# Pattern 5: Result object pattern (without exceptions)
# ============================================

class Result:
    """
    Result object pattern: encapsulates success/failure state
    """
    def __init__(self, success: bool, value: Any = None, error: str = None):
        self.success = success
        self.value = value
        self.error = error

    @classmethod
    def ok(cls, value: Any) -> 'Result':
        return cls(success=True, value=value)

    @classmethod
    def err(cls, error: str) -> 'Result':
        return cls(success=False, error=error)

    def is_ok(self) -> bool:
        return self.success

    def is_err(self) -> bool:
        return not self.success

    def unwrap(self) -> Any:
        if not self.success:
            raise ValueError(f"Attempted to unwrap an error result: {self.error}")
        return self.value

    def unwrap_or(self, default: Any) -> Any:
        return self.value if self.success else default


def safe_divide_result(a: float, b: float) -> Result:
    """
    Use result object instead of exceptions
    """
    if b == 0:
        return Result.err(f"Divisor cannot be zero: {b}")

    try:
        return Result.ok(a / b)
    except Exception as e:
        return Result.err(f"Calculation failed: {e}")


# ============================================
# Pattern 6: Collect multiple validation errors
# ============================================

class ValidationError(Exception):
    """Custom validation error"""
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__("\n".join(errors))


def validate_user(data: Dict[str, Any]) -> None:
    """
    Collect all validation errors instead of stopping at the first one
    """
    errors = []

    if 'name' not in data:
        errors.append("Missing 'name' field")
    elif not isinstance(data['name'], str):
        errors.append("'name' should be a string")
    elif len(data['name']) < 2:
        errors.append("'name' length should be at least 2")

    if 'age' not in data:
        errors.append("Missing 'age' field")
    elif not isinstance(data['age'], int):
        errors.append("'age' should be an integer")
    elif data['age'] < 0 or data['age'] > 150:
        errors.append("'age' should be between 0 and 150")

    if 'email' in data and '@' not in data['email']:
        errors.append("'email' format is invalid")

    if errors:
        raise ValidationError(errors)


# ============================================
# Pattern 7: Default values and fallbacks
# ============================================

def get_config(config: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely retrieve configuration, supports nested keys and default values
    """
    if '.' in key:
        # Support nested keys such as "database.host"
        keys = key.split('.')
        value = config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    # Simple key
    return config.get(key, default)


# ============================================
# Pattern 8: Graceful degradation
# ============================================

def get_user_preferences(user_id: int) -> Dict[str, Any]:
    """
    Try multiple methods to get user preferences, with graceful degradation
    """
    # Attempt 1: get from cache
    try:
        return _get_from_cache(user_id)
    except Exception as e:
        logger.warning(f"Failed to get from cache: {e}")

    # Attempt 2: get from database
    try:
        return _get_from_database(user_id)
    except Exception as e:
        logger.warning(f"Failed to get from database: {e}")

    # Attempt 3: use default configuration
    logger.info("Using default configuration")
    return _get_default_preferences()


def _get_from_cache(user_id: int) -> Dict[str, Any]:
    # Simulate cache failure
    raise ConnectionError("Cache connection failed")


def _get_from_database(user_id: int) -> Dict[str, Any]:
    # Simulate database failure
    raise ConnectionError("Database connection failed")


def _get_default_preferences() -> Dict[str, Any]:
    return {
        "theme": "light",
        "language": "en",
        "notifications": True
    }


# ============================================
# Test code
# ============================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=" * 50)
    print("Error Handling Pattern Examples")
    print("=" * 50)

    # Test result object pattern
    print("\n1. Result object pattern:")
    result1 = safe_divide_result(10, 2)
    print(f"10 / 2 = {result1.unwrap()}")

    result2 = safe_divide_result(10, 0)
    print(f"10 / 0 = {result2.unwrap_or('N/A')} ({result2.error})")

    # Test graceful degradation
    print("\n2. Graceful degradation:")
    prefs = get_user_preferences(123)
    print(f"User preferences: {prefs}")

    # Test context manager
    print("\n3. Context manager:")
    try:
        with DatabaseConnection("localhost:5432") as conn:
            print(f"Connection: {conn}")
    except Exception as e:
        print(f"Operation failed: {e}")
