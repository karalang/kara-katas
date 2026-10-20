# Runs data/requests/ through Python 3.13's xmlrpc: what loads() makes of
# each body, and the response SimpleXMLRPCDispatcher sends back from a
# small service. Prints what expected.out holds; run it from the app
# directory, after mk.py.
import os
import xmlrpc.client
from datetime import timedelta
from xmlrpc.client import Fault
from xmlrpc.server import SimpleXMLRPCDispatcher

store = {}


def add(a, b):
    """Return a + b."""
    return a + b


def div(a, b):
    """Return a / b."""
    return a / b


def total(values):
    """Return the sum of a list of numbers."""
    return sum(values)


def join(sep, items):
    """Join strings with a separator."""
    return sep.join(items)


def split(text, sep):
    """Split a string on a separator, or on runs of whitespace."""
    return text.split(sep)


def put(key, value):
    """Store a value under a key."""
    if not isinstance(key, str):
        raise Fault(400, "key must be a string")
    store[key] = value
    return True


def get(key):
    """Return the value stored under a key."""
    if not isinstance(key, str):
        raise Fault(400, "key must be a string")
    if key not in store:
        raise Fault(404, "no such key: %r" % key)
    return store[key]


def pop(key):
    """Remove a key and return its value."""
    if not isinstance(key, str):
        raise Fault(400, "key must be a string")
    if key not in store:
        raise Fault(404, "no such key: %r" % key)
    return store.pop(key)


def keys():
    """Return the stored keys in order."""
    return sorted(store)


def concat(blobs):
    """Join a list of byte strings."""
    return b"".join(blobs)


def size(value):
    """Return the length of a value."""
    return len(value)


def shift(when, days, seconds):
    """Move a time by a number of days and seconds."""
    return when + timedelta(days=days, seconds=seconds)


def void():
    """Return nothing."""
    return None


def echo(*args):
    """Return the arguments as a list."""
    return list(args)


server = SimpleXMLRPCDispatcher(allow_none=False, encoding=None, use_builtin_types=True)
for name, f in [("math.add", add), ("math.div", div), ("math.sum", total), ("text.join", join),
                ("text.split", split), ("kv.put", put), ("kv.get", get), ("kv.pop", pop),
                ("kv.keys", keys), ("blob.concat", concat), ("blob.size", size),
                ("time.shift", shift), ("sys.void", void), ("echo", echo)]:
    server.register_function(f, name)
server.register_introspection_functions()
server.register_multicall_functions()

for name in sorted(os.listdir("data/requests")):
    with open("data/requests/" + name, "rb") as f:
        body = f.read()
    print("== " + name)
    try:
        params, method = xmlrpc.client.loads(body, use_builtin_types=True)
        print("loads %r %r" % (method, params))
    except Fault as e:
        print("loads ! Fault %r %r" % (e.faultCode, e.faultString))
    except Exception as e:
        print("loads ! %s: %s" % (type(e).__name__, e))
    out = server._marshaled_dispatch(body).decode("utf-8")
    for line in out.split("\n"):
        print("| " + line)
