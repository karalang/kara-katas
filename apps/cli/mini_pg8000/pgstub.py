# Loads the vendored pg8000 subset (core, native, dbapi's paramstyle
# converter, converters, types) without its package __init__, which imports
# the legacy interface, together with the vendored scramp and dateutil.
# Neither is installed, so importlib.metadata.version() is answered for the
# three of them; six (which dateutil uses) and asn1crypto (which scramp
# imports for TLS channel binding, never used here since no session runs
# over TLS) get stand-ins with the few names they read. The SCRAM client
# nonce, normally a fresh uuid4, comes from NONCES in order, so the
# recorded server replies can carry the matching signatures.
import _thread
import importlib.metadata
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
VENDOR = os.path.join(HERE, 'vendor')

VERSIONS = {'pg8000': '1.31.2', 'scramp': '1.4.5', 'python-dateutil': '2.9.0.post0'}

NONCES = ['%032x' % (0x5f3a91c2d8e64b07a1c39e2f4d6b8a10 + 7919 * k) for k in range(64)]
_nonce_at = [0]


def next_nonce():
    n = NONCES[_nonce_at[0]]
    _nonce_at[0] += 1
    return n


def _add_metaclass(metaclass):
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        orig_vars['__qualname__'] = cls.__qualname__
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


def _raise_from(value, from_value):
    raise value from from_value


def install():
    real_version = importlib.metadata.version

    def version(name):
        if name in VERSIONS:
            return VERSIONS[name]
        return real_version(name)

    importlib.metadata.version = version

    six = types.ModuleType('six')
    six.PY2 = False
    six.PY3 = True
    six.text_type = str
    six.binary_type = bytes
    six.string_types = (str,)
    six.integer_types = (int,)
    six.add_metaclass = _add_metaclass
    six.raise_from = _raise_from
    moves = types.ModuleType('six.moves')
    moves._thread = _thread
    six.moves = moves
    sys.modules['six'] = six
    sys.modules['six.moves'] = moves

    asn1 = types.ModuleType('asn1crypto')
    x509 = types.ModuleType('asn1crypto.x509')

    class Certificate:
        pass

    x509.Certificate = Certificate
    asn1.x509 = x509
    sys.modules['asn1crypto'] = asn1
    sys.modules['asn1crypto.x509'] = x509

    pkg = types.ModuleType('pg8000')
    pkg.__path__ = [os.path.join(VENDOR, 'pg8000')]
    sys.modules['pg8000'] = pkg
    sys.path.insert(0, VENDOR)

    import scramp.core
    scramp.core._make_nonce = next_nonce
