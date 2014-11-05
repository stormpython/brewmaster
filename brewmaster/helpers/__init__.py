# BrewMaster Helper Functions


def for_each(iterator, f, *args):
    """Higher order function that abstracts a for in loop"""
    for item in iterator:
        f(item, *args)


def create_kwargs(key, iterator, kwargs):
    """Creates an entry in a dictionary (kwargs) based on a key
       and its corresponding value in a supplied dictionary (iterator)"""
    if key in iterator:
        kwargs[key] = iterator[key]
    else:
        kwargs[key] = None

    return kwargs
