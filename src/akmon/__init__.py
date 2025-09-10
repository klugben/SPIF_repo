"""
AkMon - AkShare驱动的期货监控与提醒系统
"""

__version__ = "0.1.0"
__author__ = "AkMon Team"
__email__ = "contact@akmon.com"

from .app import AkMonApp, Config, BasisData, AlertThreshold

__all__ = [
    "AkMonApp",
    "Config", 
    "BasisData",
    "AlertThreshold"
]
