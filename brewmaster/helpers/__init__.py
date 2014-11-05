# Notes to come
def for_each(iterator, f, *args):
    for item in iterator:
        f(item, *args)


def create_kwargs(key, iterator, kwargs):
    if key in iterator:
        kwargs[key] = iterator[key]
    else:
        kwargs[key] = None

    return kwargs
