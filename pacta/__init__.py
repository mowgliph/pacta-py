"""
PACTA - Aplicación web para la gestión de contratos y acuerdos.
"""

# Importar componentes principales
from .components import *
from .pages import *
from .state import *
from .styles import *
from .utils import *

# Exportar la aplicación principal
from .pacta import app

__all__ = [
    'app',
]