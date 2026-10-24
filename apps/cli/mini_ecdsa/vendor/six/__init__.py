# A Python 3 stand-in for the parts of six that the vendored ecdsa imports.
# It is not six: this kata does not vendor six, and runs on Python 3 only.
import struct

PY2 = False
PY3 = True
text_type = str
binary_type = bytes
integer_types = (int,)
int2byte = struct.Struct(">B").pack
next = next


def b(s):
    return s.encode("latin-1")


def python_2_unicode_compatible(klass):
    return klass
