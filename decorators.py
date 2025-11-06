from functools import wraps

def input_error(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            return "Not enough arguments"
        except (KeyError, AttributeError):
            return "Contact not found"
        except TypeError:
            return "Invalid type"
        except Exception:
            return "Internal server error"

    return wrapper