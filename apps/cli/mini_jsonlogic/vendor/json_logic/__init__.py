# Not the package's own __init__.py, which also imports its certLogic
# dialect: just the jsonLogic entry point (apply.py, builtins.py and
# types.py are panzi-json-logic 1.0.1's, verbatim).
from .apply import apply as jsonLogic

__all__ = 'jsonLogic',
