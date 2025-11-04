from functools import wraps
import traceback

def input_error(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            print(traceback.format_exc())
            return "Not enough arguments"
        except (KeyError, AttributeError):
            print(traceback.format_exc())
            return "Contact not found"
        except TypeError:
            print(traceback.format_exc())
            return "Invalid type"
        except Exception:
            print(traceback.format_exc())
            return "Internal server error"

    return wrapper