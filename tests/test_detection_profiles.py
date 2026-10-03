from dataclasses import FrozenInstanceError
from fractions import Fraction
from itertools import product
from math import gcd

import pytest

from modular_error_detection import (
    ordered_unequal_digit_pair_count,
    reduced_divisor,
    stabilized_reduced_divisor,
    stabilization_position,
    substitution_length_profile,
    substitution_position_profile,
    transposition_length_profile,
    transposition_position_profile,
)
from modular_error_detection.errors import (
    adjacent_transpositions,
    single_digit_substitutions,
)


MODULI = (2, 3, 5, 9, 10, 11, 12, 18, 25, 30, 31)


def factor_components(modulus):
    remaining = modulus
    factors = []
    for prime in (2, 3, 5):
        exponent = 0
        while remaining % prime == 0:
            exponent += 1
            remaining //= prime
        factors.append(exponent)
    return (*factors, remaining)


@pytest.mark.parametrize(
    ("divisor", "expected"),
    [(1, 90), (2, 40), (3, 24), (4, 16), (5, 10), (6, 8),
     (7, 6), (8, 4), (9, 2), (10, 0), (11, 0)],
)
def test_ordered_unequal_digit_pair_count(divisor, expected):
    assert ordered_unequal_digit_pair_count(divisor) == expected
    assert (expected == 0) is (divisor > 9)


def test_reduced_divisor_matches_gcd_factorization_for_requested_grid():
    for modulus in MODULI:
        a, b, c, u = factor_components(modulus)
        assert gcd(u, 30) == 1
        for position in range(4):
            substitution_gcd = (
                2 ** min(a, position) * 5 ** min(c, position)
            )
            transposition_gcd = (
                2 ** min(a, position)
                * 3 ** min(b, 2)
                * 5 ** min(c, position)
            )
            assert gcd(modulus, 10**position) == substitution_gcd
            assert gcd(modulus, 9 * 10**position) == transposition_gcd
            assert reduced_divisor(modulus, 1, position) == modulus // substitution_gcd
            assert reduced_divisor(modulus, 9, position) == modulus // transposition_gcd
            for profile in (
                substitution_position_profile(modulus, position),
                transposition_position_profile(modulus, position),
            ):
                h = profile.reduced_divisor
                assert profile.undetected_digit_pairs == (
                    ordered_unequal_digit_pair_count(h)
                )
                assert profile.detected_digit_pairs == 90 - profile.undetected_digit_pairs
                assert profile.universal_detection is (h > 9)
                assert profile.minimum_undetected_difference == (
                    h if h <= 9 else None
                )


def test_position_profiles_for_key_moduli():
    assert substitution_position_profile(11, 3).reduced_divisor == 11
    assert transposition_position_profile(11, 3).reduced_divisor == 11
    assert substitution_position_profile(11, 3).universal_detection
    assert transposition_position_profile(11, 3).universal_detection

    mod9 = substitution_position_profile(9, 2)
    assert mod9.undetected_digit_pairs == 2
    assert mod9.detected_digit_pairs == 88
    assert mod9.detection_rate == Fraction(44, 45)
    assert mod9.minimum_undetected_difference == 9
    assert transposition_position_profile(9, 2).undetected_digit_pairs == 90

    mod3 = substitution_position_profile(3, 1)
    assert mod3.undetected_digit_pairs == 24
    assert mod3.detected_digit_pairs == 66
    assert mod3.detection_rate == Fraction(11, 15)
    assert transposition_position_profile(3, 1).detection_rate == 0

    mod25 = substitution_position_profile(25, 1)
    assert mod25.reduced_divisor == 5
    assert mod25.undetected_digit_pairs == 10
    assert substitution_position_profile(25, 2).reduced_divisor == 1

    mod31 = substitution_position_profile(31, 3)
    assert mod31.reduced_divisor == 31
    assert mod31.universal_detection
    assert mod31.undetected_digit_pairs == 0
    assert ordered_unequal_digit_pair_count(11) == 0


@pytest.mark.parametrize("modulus", MODULI)
def test_stabilization_matches_factorization(modulus):
    a, b, c, u = factor_components(modulus)
    threshold = max(a, c)
    assert stabilization_position(modulus, "substitution") == threshold
    assert stabilization_position(modulus, "transposition") == threshold
    assert stabilized_reduced_divisor(modulus, "substitution") == 3**b * u
    assert stabilized_reduced_divisor(modulus, "transposition") == (
        3 ** max(b - 2, 0) * u
    )
    for error_class, coefficient in (("substitution", 1), ("transposition", 9)):
        stable = stabilized_reduced_divisor(modulus, error_class)
        assert reduced_divisor(modulus, coefficient, threshold) == stable
        assert reduced_divisor(modulus, coefficient, threshold + 1) == stable
        assert reduced_divisor(modulus, coefficient, threshold + 3) == stable
        if threshold:
            assert reduced_divisor(modulus, coefficient, threshold - 1) != stable


@pytest.mark.parametrize(
    ("modulus", "substitution", "transposition"),
    [(11, True, True), (9, False, False), (3, False, False),
     (25, False, False), (31, True, True)],
)
def test_all_finite_length_universal_detection(modulus, substitution, transposition):
    assert (
        stabilized_reduced_divisor(modulus, "substitution") > 9
    ) is substitution
    assert (
        stabilized_reduced_divisor(modulus, "transposition") > 9
    ) is transposition


def test_fixed_length_profiles_keep_pair_and_full_event_counts_distinct():
    substitution = substitution_length_profile(9, 2)
    assert substitution.total_events == 1800
    assert substitution.undetected_events == 40
    assert substitution.detected_events == 1760
    assert substitution.detection_rate == Fraction(44, 45)
    assert [row.total_events for row in substitution.positions] == [900, 900]
    assert [row.position_profile.undetected_digit_pairs for row in substitution.positions] == [2, 2]
    assert [row.undetected_events for row in substitution.positions] == [20, 20]

    transposition = transposition_length_profile(11, 2)
    assert transposition.total_events == 90
    assert transposition.detected_events == 90
    assert transposition.undetected_events == 0
    assert transposition.detection_rate == Fraction(1, 1)
    assert len(transposition.positions) == 1


def test_only_transposition_length_profiles_require_two_digits():
    assert substitution_length_profile(11, 1).total_events == 90
    with pytest.raises(ValueError, match="length must be at least 2"):
        transposition_length_profile(11, 1)


def test_profile_results_are_immutable():
    profile = substitution_position_profile(11, 0)
    with pytest.raises(FrozenInstanceError):
        profile.reduced_divisor = 1
    length_profile = substitution_length_profile(11, 2)
    with pytest.raises(FrozenInstanceError):
        length_profile.positions = ()


@pytest.mark.parametrize("modulus", [0, 1, -2, True, 2.5])
def test_invalid_modulus_rejected(modulus):
    with pytest.raises((TypeError, ValueError)):
        substitution_position_profile(modulus, 0)


@pytest.mark.parametrize("position", [-1, True, 1.5])
def test_invalid_position_rejected(position):
    with pytest.raises((TypeError, ValueError)):
        reduced_divisor(11, 1, position)


def direct_position_counts(modulus, length, error_class):
    positions = length if error_class == "substitution" else length - 1
    totals = [0] * positions
    detected = [0] * positions
    generator = (
        single_digit_substitutions
        if error_class == "substitution"
        else adjacent_transpositions
    )
    for digit_tuple in product("0123456789", repeat=length):
        original = "".join(digit_tuple)
        original_residue = int(original) % modulus
        for altered in generator(original):
            changed = [
                index
                for index, (first, second) in enumerate(zip(original, altered))
                if first != second
            ]
            position = (
                length - 1 - changed[0]
                if error_class == "substitution"
                else length - 2 - changed[0]
            )
            totals[position] += 1
            detected[position] += int(int(altered) % modulus != original_residue)
    return totals, detected


@pytest.mark.parametrize("modulus", [3, 9, 11, 25, 31])
@pytest.mark.parametrize("length", [1, 2, 3])
@pytest.mark.parametrize("error_class", ["substitution", "transposition"])
def test_analytical_profiles_cross_check_against_direct_event_enumeration(
    modulus, length, error_class
):
    if error_class == "transposition" and length == 1:
        return
    profile = (
        substitution_length_profile(modulus, length)
        if error_class == "substitution"
        else transposition_length_profile(modulus, length)
    )
    direct_totals, direct_detected = direct_position_counts(
        modulus, length, error_class
    )
    assert profile.total_events == sum(direct_totals)
    assert profile.detected_events == sum(direct_detected)
    assert profile.undetected_events == profile.total_events - profile.detected_events
    assert profile.detection_rate == Fraction(profile.detected_events, profile.total_events)
    for row, total, detected in zip(profile.positions, direct_totals, direct_detected):
        assert row.total_events == total
        assert row.detected_events == detected
        assert row.undetected_events == total - detected
        assert row.detection_rate == Fraction(detected, total)
