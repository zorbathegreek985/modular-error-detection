"""Exact analytical profiles for decimal modular-residue error detection."""

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Literal

ErrorClass = Literal["substitution", "transposition"]


@dataclass(frozen=True, slots=True)
class PositionProfile:
    """Digit-pair detection behavior for one error class and position."""

    modulus: int
    position: int
    error_class: ErrorClass
    reduced_divisor: int
    undetected_digit_pairs: int
    detected_digit_pairs: int
    detection_rate: Fraction
    undetection_rate: Fraction
    universal_detection: bool
    minimum_undetected_difference: int | None


@dataclass(frozen=True, slots=True)
class LengthPositionProfile:
    """Full-string event counts for one position in a fixed-width string."""

    length: int
    position_profile: PositionProfile
    total_events: int
    detected_events: int
    undetected_events: int
    detection_rate: Fraction
    undetection_rate: Fraction


@dataclass(frozen=True, slots=True)
class LengthProfile:
    """Exact event totals and rates across all positions at one length."""

    modulus: int
    length: int
    error_class: ErrorClass
    positions: tuple[LengthPositionProfile, ...]
    total_events: int
    detected_events: int
    undetected_events: int
    detection_rate: Fraction
    undetection_rate: Fraction
    universal_detection: bool


def _positive_integer(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer (not bool)")
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _modulus(value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("modulus must be an integer (not bool)")
    if value <= 1:
        raise ValueError("modulus must be greater than 1")


def _position(value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("position must be an integer (not bool)")
    if value < 0:
        raise ValueError("position must be nonnegative")


def _length(value: int, minimum: int = 1) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("length must be an integer (not bool)")
    if value < minimum:
        raise ValueError(f"length must be at least {minimum}")


def _coefficient(error_class: str) -> int:
    if error_class == "substitution":
        return 1
    if error_class == "transposition":
        return 9
    raise ValueError(f"unknown error class: {error_class}")


def reduced_divisor(modulus: int, coefficient: int, position: int) -> int:
    """Return ``m / gcd(m, coefficient * 10**position)`` exactly."""
    _modulus(modulus)
    _positive_integer(coefficient, "coefficient")
    _position(position)
    return modulus // gcd(modulus, coefficient * 10**position)


def ordered_unequal_digit_pair_count(reduced: int) -> int:
    """Count ordered unequal decimal pairs with difference divisible by h."""
    _positive_integer(reduced, "reduced divisor")
    return 2 * sum(
        10 - reduced * multiple
        for multiple in range(1, 9 // reduced + 1)
    )


def _position_profile(
    modulus: int, position: int, error_class: ErrorClass
) -> PositionProfile:
    coefficient = _coefficient(error_class)
    reduced = reduced_divisor(modulus, coefficient, position)
    undetected = ordered_unequal_digit_pair_count(reduced)
    detected = 90 - undetected
    return PositionProfile(
        modulus=modulus,
        position=position,
        error_class=error_class,
        reduced_divisor=reduced,
        undetected_digit_pairs=undetected,
        detected_digit_pairs=detected,
        detection_rate=Fraction(detected, 90),
        undetection_rate=Fraction(undetected, 90),
        universal_detection=undetected == 0,
        minimum_undetected_difference=reduced if undetected else None,
    )


def substitution_position_profile(modulus: int, position: int) -> PositionProfile:
    """Return exact digit-pair behavior for a substitution at ``position``."""
    return _position_profile(modulus, position, "substitution")


def transposition_position_profile(modulus: int, position: int) -> PositionProfile:
    """Return exact digit-pair behavior for a swap at lower-place ``position``."""
    return _position_profile(modulus, position, "transposition")


def _length_position(
    profile: PositionProfile, length: int, free_digits: int
) -> LengthPositionProfile:
    total = 90 * 10**free_digits
    undetected = profile.undetected_digit_pairs * 10**free_digits
    detected = total - undetected
    return LengthPositionProfile(
        length=length,
        position_profile=profile,
        total_events=total,
        detected_events=detected,
        undetected_events=undetected,
        detection_rate=Fraction(detected, total),
        undetection_rate=Fraction(undetected, total),
    )


def _length_profile(
    modulus: int, length: int, error_class: ErrorClass
) -> LengthProfile:
    _modulus(modulus)
    _length(length, minimum=2 if error_class == "transposition" else 1)
    positions_count = length if error_class == "substitution" else length - 1
    free_digits = length - (1 if error_class == "substitution" else 2)
    positions = tuple(
        _length_position(
            _position_profile(modulus, position, error_class),
            length,
            free_digits,
        )
        for position in range(positions_count)
    )
    total = sum(row.total_events for row in positions)
    detected = sum(row.detected_events for row in positions)
    undetected = total - detected
    return LengthProfile(
        modulus=modulus,
        length=length,
        error_class=error_class,
        positions=positions,
        total_events=total,
        detected_events=detected,
        undetected_events=undetected,
        detection_rate=Fraction(detected, total),
        undetection_rate=Fraction(undetected, total),
        universal_detection=undetected == 0,
    )


def substitution_length_profile(modulus: int, length: int) -> LengthProfile:
    """Return exact substitution events, counts, and rates for a string length."""
    return _length_profile(modulus, length, "substitution")


def transposition_length_profile(modulus: int, length: int) -> LengthProfile:
    """Return exact unequal-adjacent-swap profile; requires ``length >= 2``."""
    return _length_profile(modulus, length, "transposition")


def _factor_modulus(modulus: int) -> tuple[int, int, int, int]:
    remaining = modulus
    exponents = []
    for prime in (2, 3, 5):
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        exponents.append(exponent)
    return (*exponents, remaining)


def stabilization_position(modulus: int, error_class: ErrorClass) -> int:
    """Return the first position at which the reduced-divisor sequence stabilizes."""
    _modulus(modulus)
    _coefficient(error_class)
    a, _, c, _ = _factor_modulus(modulus)
    return max(a, c)


def stabilized_reduced_divisor(modulus: int, error_class: ErrorClass) -> int:
    """Return the eventual reduced divisor for the selected error class."""
    _modulus(modulus)
    _coefficient(error_class)
    _, b, _, u = _factor_modulus(modulus)
    if error_class == "substitution":
        return 3**b * u
    return 3 ** max(b - 2, 0) * u
