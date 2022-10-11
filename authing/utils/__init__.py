import string
import random

try:
    # python 3
    from urllib.parse import urlencode
except:
    # python 2
    from urllib import urlencode

def get_random_string(length=10):
    # type:(int) -> str
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str

def url_join_args(api, query=None, **kwargs):
    result = api
    if not result.endswith('?') and (query or kwargs):
        result = api + '?'
    if query:
        result = result + urlencode(query)
    if kwargs:
        if query:
            result = result + '&' + urlencode(kwargs)
        else:
            result = result + urlencode(kwargs)
    return result
