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
drogapl.py
==========

Main plugin class. Registers the toolbar icon / menu entry in QGIS and
shows / hides the DrogaPL dock widget.
"""

import os.path

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .gui.main_dockwidget import DrogaPLDockWidget


class DrogaPL:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this
            class which provides the hook by which you can manipulate the
            QGIS application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        # --- Internationalisation --------------------------------------
        locale = QSettings().value("locale/userLocale", "en")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", f"DrogaPL_{locale}.qm"
        )

        self.translator = None
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # --- Plugin state ------------------------------------------------
        self.actions = []
        self.menu = self.tr("&DrogaPL")
        self.toolbar = self.iface.addToolBar("DrogaPL")
        self.toolbar.setObjectName("DrogaPL")

        self.dock_widget = None
        self.dock_widget_visible = False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def tr(self, message):
        return QCoreApplication.translate("DrogaPL", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)
        return action

    # ------------------------------------------------------------------
    # QGIS plugin lifecycle
    # ------------------------------------------------------------------
    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        self.add_action(
            icon_path,
            text=self.tr("DrogaPL"),
            callback=self.toggle_dock_widget,
            parent=self.iface.mainWindow(),
            status_tip=self.tr("Otworz panel DrogaPL"),
        )

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

        if self.dock_widget is not None:
            self.iface.removeDockWidget(self.dock_widget)
            self.dock_widget = None

    # ------------------------------------------------------------------
    # Dock widget management
    # ------------------------------------------------------------------
    def toggle_dock_widget(self):
        if self.dock_widget is None:
            self.dock_widget = DrogaPLDockWidget()
            self.dock_widget.closingPlugin.connect(self._on_dock_widget_closed)
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
            self.dock_widget.show()
            self.dock_widget_visible = True
        else:
            self.dock_widget_visible = not self.dock_widget_visible
            self.dock_widget.setVisible(self.dock_widget_visible)

    def _on_dock_widget_closed(self):
        self.dock_widget_visible = False
