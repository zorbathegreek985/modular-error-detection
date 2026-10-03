"""Tools for studying modular checksum error detection."""

from .checksum import checksum, same_residue
from .profiles import (
    LengthPositionProfile,
    LengthProfile,
    PositionProfile,
    ordered_unequal_digit_pair_count,
    reduced_divisor,
    stabilized_reduced_divisor,
    stabilization_position,
    substitution_length_profile,
    substitution_position_profile,
    transposition_length_profile,
    transposition_position_profile,
)

__all__ = [
    "LengthPositionProfile",
    "LengthProfile",
    "PositionProfile",
    "checksum",
    "ordered_unequal_digit_pair_count",
    "reduced_divisor",
    "same_residue",
    "stabilized_reduced_divisor",
    "stabilization_position",
    "substitution_length_profile",
    "substitution_position_profile",
    "transposition_length_profile",
    "transposition_position_profile",
]
