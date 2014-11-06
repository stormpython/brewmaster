def for_each(iterator, f, *args):
    """Higher order function that abstracts a for in loop"""
    for item in iterator:
        f(item, *args)
