def create_kwarg(key, iterator, kwarg):
    """Creates an entry in a dictionary (`kwargs`) based on the `key`
       and its corresponding value in a supplied dictionary (`iterator`)"""
    kwarg[key] = iterator[key] if key in iterator else None

    return kwarg
