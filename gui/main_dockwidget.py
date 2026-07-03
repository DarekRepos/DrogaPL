# -*- coding: utf-8 -*-
"""
main_dockwidget.py
===================

Main dock widget for DrogaPL. Stage 0 scope: let the user pick a Polish
road technical class and see the associated design parameters, pulled
from core/standards.py.

The widget is built directly in Python (no .ui file) to keep the
skeleton dependency-free and easy to read. It can be migrated to a
Qt Designer .ui file later without changing its public interface.
"""

import os
import sys

from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import pyqtSignal

# Make sure the plugin root is importable so "from core.standards import ..."
# works regardless of how QGIS loads this module.
_PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PLUGIN_DIR not in sys.path:
    sys.path.append(_PLUGIN_DIR)

from core.standards import get_road_class_codes, get_standard  # noqa: E402


class DrogaPLDockWidget(QtWidgets.QDockWidget):
    """Dock widget showing road class selection and standard parameters."""

    # Emitted when the user closes the dock widget, so the main plugin
    # class can update its internal state (e.g. uncheck the toolbar icon).
    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("DrogaPL"))
        self.setObjectName("DrogaPLDockWidget")

        self._build_ui()
        self._populate_road_classes()
        self._on_road_class_changed(self.road_class_combo.currentText())

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        container.setLayout(layout)

        # --- Road class selection -----------------------------------
        form_layout = QtWidgets.QFormLayout()

        self.road_class_combo = QtWidgets.QComboBox()
        self.road_class_combo.currentTextChanged.connect(self._on_road_class_changed)
        form_layout.addRow(self.tr("Klasa techniczna drogi:"), self.road_class_combo)

        layout.addLayout(form_layout)

        # --- Parameters table ------------------------------------------
        self.params_table = QtWidgets.QTableWidget()
        self.params_table.setColumnCount(2)
        self.params_table.setHorizontalHeaderLabels(
            [self.tr("Parametr"), self.tr("Wartosc")]
        )
        self.params_table.horizontalHeader().setStretchLastSection(True)
        self.params_table.verticalHeader().setVisible(False)
        self.params_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.params_table)

        # --- Placeholder buttons for future stages ---------------------
        future_group = QtWidgets.QGroupBox(self.tr("Kolejne etapy (jeszcze nieaktywne)"))
        future_layout = QtWidgets.QVBoxLayout()
        future_group.setLayout(future_layout)

        for label in (
            self.tr("Rysuj os trasy"),
            self.tr("Edytuj niwelete"),
            self.tr("Generuj przekroje poprzeczne"),
            self.tr("Oblicz kubatury robot ziemnych"),
        ):
            btn = QtWidgets.QPushButton(label)
            btn.setEnabled(False)
            future_layout.addWidget(btn)

        layout.addWidget(future_group)
        layout.addStretch()

        self.setWidget(container)

    # ------------------------------------------------------------------
    # Data population / interaction
    # ------------------------------------------------------------------
    def _populate_road_classes(self):
        self.road_class_combo.clear()
        for code in get_road_class_codes():
            standard = get_standard(code)
            self.road_class_combo.addItem(f"{code} - {standard.name_pl}", userData=code)

    def _on_road_class_changed(self, _text):
        code = self.road_class_combo.currentData()
        if code is None and self.road_class_combo.count():
            # Fallback for the very first call before userData is wired up.
            code = self.road_class_combo.currentText().split(" - ")[0]
        if not code:
            return

        standard = get_standard(code)
        rows = [
            (self.tr("Predkosc projektowa (teren zabudowany)"),
             f"{standard.design_speed_kmh_builtup} km/h"),
            (self.tr("Predkosc projektowa (teren otwarty)"),
             f"{standard.design_speed_kmh_open} km/h"),
            (self.tr("Min. promien luku poziomego"),
             f"{standard.min_horizontal_radius_m} m"),
            (self.tr("Min. promien luku poziomego (wyjatkowy)"),
             f"{standard.min_horizontal_radius_exceptional_m} m"
             if standard.min_horizontal_radius_exceptional_m else "-"),
            (self.tr("Min. promien luku pionowego wypuklego"),
             f"{standard.min_vertical_radius_convex_m} m"),
            (self.tr("Min. promien luku pionowego wkleslego"),
             f"{standard.min_vertical_radius_concave_m} m"),
            (self.tr("Maks. pochylenie podluzne"),
             f"{standard.max_longitudinal_gradient_pct} %"),
            (self.tr("Min. parametr klotoidy A"),
             f"{standard.min_clothoid_parameter_a_m} m"),
        ]

        self.params_table.setRowCount(len(rows))
        for row_index, (label, value) in enumerate(rows):
            self.params_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(label))
            self.params_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(value))
        self.params_table.resizeColumnsToContents()

    # ------------------------------------------------------------------
    # Qt lifecycle
    # ------------------------------------------------------------------
    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
