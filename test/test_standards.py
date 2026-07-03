# -*- coding: utf-8 -*-
"""
Unit tests for core/standards.py.

Run with: pytest test/test_standards.py
These tests do NOT require QGIS to be installed, since core/standards.py
has no PyQt / PyQGIS dependency.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.standards import get_standard, get_road_class_codes, ROAD_CLASSES


def test_all_codes_have_a_standard():
    for code in get_road_class_codes():
        standard = get_standard(code)
        assert standard.code == code


def test_unknown_code_raises():
    try:
        get_standard("X")
        assert False, "Expected KeyError for unknown road class code"
    except KeyError:
        pass


def test_design_speed_is_positive():
    for standard in ROAD_CLASSES.values():
        assert standard.design_speed_kmh_open > 0
        assert standard.design_speed_kmh_builtup > 0


def test_radii_increase_with_class_importance():
    # Sanity check: higher class roads (A, S) should require larger
    # minimum radii than lower class roads (L, D).
    a = get_standard("A")
    d = get_standard("D")
    assert a.min_horizontal_radius_m > d.min_horizontal_radius_m
    assert a.min_vertical_radius_convex_m > d.min_vertical_radius_convex_m
