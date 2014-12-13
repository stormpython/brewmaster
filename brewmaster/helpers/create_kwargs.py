###############################################################################
# This helper function creates a dictionary of keys and appropriately modified
# MySQL responses as their values. Some MySQL responses are returned as
# dictionaries, which need to be modified (json.dumps). Others are returned
# as strings, which need escaping (escape_string). Finally, some values for
# keys are not present and need to be given the special value `None`.
###############################################################################

import json
from pymysql import escape_string


def create_kwargs(key, iterator, kwargs):
    """Callback function that returns a dictionary of keys with appropriately
    modified value pairs.
    """
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
