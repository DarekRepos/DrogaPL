# -*- coding: utf-8 -*-
"""
standards.py
============

Data module holding Polish technical requirements for public roads,
based on the Regulation of the Minister of Infrastructure on technical
conditions to be met by public roads and their location
(Rozporzadzenie Ministra Infrastruktury z dnia 3 lipca 2003 r., z pozn. zm.,
tekst jednolity Dz.U. 2016 poz. 124) and GDDKiA design guidelines (WR-D).

IMPORTANT
---------
The numeric values below are placeholders meant to establish the data
structure and let the rest of the plugin (GUI, validation logic) be built
and tested. Before relying on this module for real design work, every
value must be checked and corrected against the current, official text of
the regulation and any amendments, since technical requirements can change
over time and vary with additional conditions (terrain type, urban vs.
rural cross-section, etc.) not modeled here yet.

This module intentionally has zero dependency on PyQt / PyQGIS so it can
be unit tested with plain pytest, without a running QGIS instance.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class RoadClassStandard:
    """Technical parameters associated with one Polish road technical class."""

    # Road technical class code, e.g. "A", "S", "GP", "G", "Z", "L", "D"
    code: str

    # Human readable name (Polish), e.g. "droga ekspresowa"
    name_pl: str

    # Design speed in built-up / open area [km/h]
    design_speed_kmh_builtup: int
    design_speed_kmh_open: int

    # Minimum horizontal curve radius, normal case [m]
    min_horizontal_radius_m: int

    # Minimum horizontal curve radius, exceptional case (allowed with
    # justification, superelevation at max value) [m]
    min_horizontal_radius_exceptional_m: Optional[int]

    # Minimum convex (crest) vertical curve radius [m]
    min_vertical_radius_convex_m: int

    # Minimum concave (sag) vertical curve radius [m]
    min_vertical_radius_concave_m: int

    # Maximum longitudinal gradient [%]
    max_longitudinal_gradient_pct: float

    # Minimum transition curve (clothoid) parameter A, rule-of-thumb
    # lower bound often expressed as A >= R / 3 ... R; kept here as a
    # simple minimum value to be refined per radius later.
    min_clothoid_parameter_a_m: int


# Placeholder table - VERIFY against the official regulation before use.
ROAD_CLASSES: Dict[str, RoadClassStandard] = {
    "A": RoadClassStandard(
        code="A",
        name_pl="autostrada",
        design_speed_kmh_builtup=80,
        design_speed_kmh_open=120,
        min_horizontal_radius_m=600,
        min_horizontal_radius_exceptional_m=430,
        min_vertical_radius_convex_m=10000,
        min_vertical_radius_concave_m=4000,
        max_longitudinal_gradient_pct=4.0,
        min_clothoid_parameter_a_m=200,
    ),
    "S": RoadClassStandard(
        code="S",
        name_pl="droga ekspresowa",
        design_speed_kmh_builtup=70,
        design_speed_kmh_open=100,
        min_horizontal_radius_m=400,
        min_horizontal_radius_exceptional_m=280,
        min_vertical_radius_convex_m=6000,
        min_vertical_radius_concave_m=2500,
        max_longitudinal_gradient_pct=5.0,
        min_clothoid_parameter_a_m=150,
    ),
    "GP": RoadClassStandard(
        code="GP",
        name_pl="droga glowna ruchu przyspieszonego",
        design_speed_kmh_builtup=60,
        design_speed_kmh_open=80,
        min_horizontal_radius_m=250,
        min_horizontal_radius_exceptional_m=150,
        min_vertical_radius_convex_m=3000,
        min_vertical_radius_concave_m=1500,
        max_longitudinal_gradient_pct=6.0,
        min_clothoid_parameter_a_m=100,
    ),
    "G": RoadClassStandard(
        code="G",
        name_pl="droga glowna",
        design_speed_kmh_builtup=50,
        design_speed_kmh_open=70,
        min_horizontal_radius_m=200,
        min_horizontal_radius_exceptional_m=120,
        min_vertical_radius_convex_m=2000,
        min_vertical_radius_concave_m=1000,
        max_longitudinal_gradient_pct=7.0,
        min_clothoid_parameter_a_m=70,
    ),
    "Z": RoadClassStandard(
        code="Z",
        name_pl="droga zbiorcza",
        design_speed_kmh_builtup=40,
        design_speed_kmh_open=60,
        min_horizontal_radius_m=125,
        min_horizontal_radius_exceptional_m=75,
        min_vertical_radius_convex_m=1000,
        min_vertical_radius_concave_m=600,
        max_longitudinal_gradient_pct=8.0,
        min_clothoid_parameter_a_m=50,
    ),
    "L": RoadClassStandard(
        code="L",
        name_pl="droga lokalna",
        design_speed_kmh_builtup=30,
        design_speed_kmh_open=50,
        min_horizontal_radius_m=75,
        min_horizontal_radius_exceptional_m=50,
        min_vertical_radius_convex_m=600,
        min_vertical_radius_concave_m=375,
        max_longitudinal_gradient_pct=9.0,
        min_clothoid_parameter_a_m=30,
        ),
    "D": RoadClassStandard(
        code="D",
        name_pl="droga dojazdowa",
        design_speed_kmh_builtup=30,
        design_speed_kmh_open=40,
        min_horizontal_radius_m=30,
        min_horizontal_radius_exceptional_m=20,
        min_vertical_radius_convex_m=300,
        min_vertical_radius_concave_m=250,
        max_longitudinal_gradient_pct=10.0,
        min_clothoid_parameter_a_m=20,
    ),
}


def get_road_class_codes():
    """Return the list of available road class codes, in a sensible order."""
    return ["A", "S", "GP", "G", "Z", "L", "D"]


def get_standard(code: str) -> RoadClassStandard:
    """Return the RoadClassStandard for a given road class code.

    :param code: Road class code, e.g. "GP".
    :raises KeyError: if the code is not a recognised road class.
    """
    try:
        return ROAD_CLASSES[code]
    except KeyError as exc:
        raise KeyError(
            f"Unknown road class code: {code!r}. "
            f"Valid codes are: {', '.join(get_road_class_codes())}"
        ) from exc
