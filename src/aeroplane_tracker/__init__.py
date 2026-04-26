"""
Aeroplane Tracker Package
Отслеживание самолетов через OpenSky Network API
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__all__ = ['Aeroplane', 'AeroplanesAPI', 'JSONSaver']

from .aeroplane import Aeroplane
from .api_client import AeroplanesAPI
from .json_storage import JSONSaver
