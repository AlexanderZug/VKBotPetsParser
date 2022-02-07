
def error_handler(func):
    def wrapper(*args, **kvargs):
        try:
            return func(*args, **kvargs)
        except Exception:
            pass
    return wrapper
