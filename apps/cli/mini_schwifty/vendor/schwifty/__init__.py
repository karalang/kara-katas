from importlib.metadata import version

from schwifty.bban import BBAN
from schwifty.bic import BIC
from schwifty.iban import IBAN


__all__ = [
    "BBAN",
    "BIC",
    "IBAN",
]
try:
    __version__ = version(__name__)
except Exception:  # vendored copy has no installed dist metadata
    __version__ = "2026.10.0"
