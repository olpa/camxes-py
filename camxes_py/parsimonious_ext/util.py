
# pylint: disable=I0011, C0111, C0326, too-many-arguments, protected-access

"""
Decorators for making ugly hacks look less ugly.
"""

def add_to_class(cls):
    """Add method, replacing any previous method by name"""
    def decorator(decorated):
        setattr(cls, decorated.__name__, decorated)
        return decorated
    return decorator

def with_original(original_function):
    if hasattr(original_function, '__func__'): # unwrap python 2 unbound methods
        original_function = original_function.__func__
    def decorator(decorated):
        decorated = partial(decorated, original=original_function)
        @wraps(original_function)
        def decoration(self, *args, **kwargs):
            return decorated(self, *args, **kwargs)
        return decoration
    return decorator

def renamed(new_name):
    def decorator(decorated):
        decorated.__name__ = new_name
        return decorated
    return decorator

