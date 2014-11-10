import json
from pymysql import escape_string


def create_kwargs(key, iterator, kwargs):
    if key in iterator:
        value = iterator[key]

        if isinstance(value, dict):
            kwargs[key] = json.dumps(value)
        elif isinstance(value, str):
            kwargs[key] = escape_string(value)
        else:
            kwargs[key] = iterator[key]
    else:
        kwargs[key] = None

    return kwargs
