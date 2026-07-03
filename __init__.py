# -*- coding: utf-8 -*-
"""
DrogaPL
=======

QGIS plugin for road geometric design following Polish technical standards.

This file is required by QGIS. It must contain a classFactory function
that QGIS calls to instantiate the plugin.
"""


def classFactory(iface):
    """Load DrogaPL class from file drogapl.py.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .drogapl import DrogaPL
    return DrogaPL(iface)
