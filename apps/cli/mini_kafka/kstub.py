# Loads the vendored kafka-python subset without its package __init__ (which
# imports the client, consumer and producer) and without six: the modules
# that use six get a stand-in with the few names they read. The optional
# codec libraries are blocked, so snappy, lz4 and zstd report themselves
# missing, as on a plain install.
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))


def _add_metaclass(metaclass):
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        orig_vars['__qualname__'] = cls.__qualname__
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


def install():
    for name in ('snappy', 'zstandard', 'lz4', 'lz4.frame', 'lz4f',
                 'lz4framed', 'xxhash', 'crc32c', 'numpy'):
        sys.modules[name] = None
    pkg = types.ModuleType('kafka')
    pkg.__path__ = [os.path.join(HERE, 'vendor', 'kafka')]
    sys.modules['kafka'] = pkg
    vendor = types.ModuleType('kafka.vendor')
    vendor.__path__ = []
    six = types.ModuleType('kafka.vendor.six')
    six.PY2 = False
    six.PY3 = True
    six.string_types = (str,)
    six.add_metaclass = _add_metaclass
    moves = types.ModuleType('kafka.vendor.six.moves')
    moves.range = range
    six.moves = moves
    vendor.six = six
    pkg.vendor = vendor
    sys.modules['kafka.vendor'] = vendor
    sys.modules['kafka.vendor.six'] = six
    sys.modules['kafka.vendor.six.moves'] = moves
