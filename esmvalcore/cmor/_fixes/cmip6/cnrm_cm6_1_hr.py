"""Fixes for CNRM-CM6-1-HR model."""
from .cnrm_cm6_1 import Cl as BaseCl


class Cl(BaseCl):
    """Fixes for ``cl``."""


class Clw(Cl):
    """Fixes for ``clw (same as for cl)``."""


class Cli(Cl):
    """Fixes for ``cli (same as for cl)``."""
