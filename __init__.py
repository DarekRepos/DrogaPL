# -*- coding: utf-8 -*-
# Copyright (C) 2026 Your Name
# This plugin is licensed under the GNU General Public License v3 or later.
#
# DrogaPL is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This plugin is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this plugin. If not, see <https://www.gnu.org/licenses/>.

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
