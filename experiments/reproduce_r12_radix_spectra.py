"""Print the bounded radix-spectrum class counts reported in research/R12."""

import csv
import sys
from dataclasses import dataclass

from modular_error_detection.radix_spectra import (
    enumerate_radix_spectrum_classes,
    radix_stabilization_position,
)


RADICES = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 20)
MINIMUM_MODULUS = 2
MAXIMUM_MODULUS = 5000


@dataclass(frozen=True, slots=True)
class RadixSummary:
    radix: int
    max_position: int
    moduli_examined: int
    substitution_classes: int
    transposition_classes: int
    joint_classes: int
    zero_joint_moduli: int


def calculate_radix_summary(
    radix: int, minimum_modulus: int, maximum_modulus: int
) -> RadixSummary:
    """Compute all R12 class statistics for one bounded radix domain."""
    max_position = max(
        radix_stabilization_position(radix, modulus)
        for modulus in range(minimum_modulus, maximum_modulus + 1)
    )
    substitutions = enumerate_radix_spectrum_classes(
        radix,
        minimum_modulus,
        maximum_modulus,
        max_position,
        include_transposition=False,
    )
    transpositions = enumerate_radix_spectrum_classes(
        radix,
        minimum_modulus,
        maximum_modulus,
        max_position,
        include_substitution=False,
    )
    joint = enumerate_radix_spectrum_classes(
        radix, minimum_modulus, maximum_modulus, max_position
    )
    zero_joint = next(group for group in joint.classes if not any(group.spectrum_key))
    return RadixSummary(
        radix=radix,
        max_position=max_position,
        moduli_examined=joint.moduli_examined,
        substitution_classes=substitutions.class_count,
        transposition_classes=transpositions.class_count,
        joint_classes=joint.class_count,
        zero_joint_moduli=zero_joint.size,
    )


def main() -> int:
    """Write a deterministic CSV table to standard output."""
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(
        (
            "radix",
            "minimum_modulus",
            "maximum_modulus",
            "max_position_inclusive",
            "moduli_examined",
            "substitution_classes",
            "transposition_classes",
            "joint_classes",
            "zero_joint_moduli",
        )
    )
    for radix in RADICES:
        summary = calculate_radix_summary(
            radix, MINIMUM_MODULUS, MAXIMUM_MODULUS
        )
        writer.writerow(
            (
                summary.radix,
                MINIMUM_MODULUS,
                MAXIMUM_MODULUS,
                summary.max_position,
                summary.moduli_examined,
                summary.substitution_classes,
                summary.transposition_classes,
                summary.joint_classes,
                summary.zero_joint_moduli,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
