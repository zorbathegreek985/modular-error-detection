import pytest

from modular_error_detection.radix_spectra import (
    enumerate_radix_spectrum_classes,
    radix_pair_weight,
    radix_stabilization_position,
    radix_substitution_spectrum,
    radix_transposition_spectrum,
)


def test_single_modulus_enumeration_is_deterministic():
    first = enumerate_radix_spectrum_classes(10, 14, 14, 2)
    second = enumerate_radix_spectrum_classes(10, 14, 14, 2)

    assert first == second
    assert first.moduli_examined == 1
    assert first.class_count == 1
    assert first.classes[0].representative_modulus == 14
    assert first.classes[0].moduli == (14,)
    assert first.classes[0].spectrum_key == (0, 6, 6, 0, 6, 6)


def test_decimal_moduli_14_and_35_have_equal_joint_spectra():
    result = enumerate_radix_spectrum_classes(10, 14, 35, 2)
    classes = [group for group in result.classes if 14 in group.moduli or 35 in group.moduli]

    assert len(classes) == 1
    assert {14, 35}.issubset(classes[0].moduli)
    assert classes[0].spectrum_key == (0, 6, 6, 0, 6, 6)


def test_different_joint_spectra_are_separate_classes():
    result = enumerate_radix_spectrum_classes(10, 11, 21, 2)
    class_for_11 = next(group for group in result.classes if 11 in group.moduli)
    class_for_21 = next(group for group in result.classes if 21 in group.moduli)

    assert class_for_11 is not class_for_21
    assert class_for_11.spectrum_key != class_for_21.spectrum_key


def test_radix_11_documented_transposition_equivalence():
    result = enumerate_radix_spectrum_classes(
        11, 14, 35, 2, include_substitution=False
    )
    group = next(group for group in result.classes if 14 in group.moduli)

    assert 35 in group.moduli
    assert group.spectrum_key == (8, 8, 8)
    assert radix_transposition_spectrum(11, 14, 2) == (8, 8, 8)
    assert radix_substitution_spectrum(11, 14, 2) == (0, 0, 0)


def test_class_membership_matches_observable_keys():
    result = enumerate_radix_spectrum_classes(4, 2, 20, 3)
    by_modulus = {
        modulus: group
        for group in result.classes
        for modulus in group.moduli
    }

    assert set(by_modulus) == set(range(2, 21))
    for first in range(2, 21):
        for second in range(2, 21):
            same_key = by_modulus[first].spectrum_key == by_modulus[second].spectrum_key
            same_class = by_modulus[first] is by_modulus[second]
            assert same_class is same_key


def test_q2_bounded_class_counts_match_r11_table():
    result = enumerate_radix_spectrum_classes(2, 2, 1000, 9)

    assert result.moduli_examined == 999
    assert result.class_count == 10
    zero_class = next(group for group in result.classes if not any(group.spectrum_key))
    assert zero_class.size == 990
    assert zero_class.representative_modulus == 3


def direct_pair_spectrum(radix, modulus, max_position, *, transposition):
    values = []
    for position in range(max_position + 1):
        undetected = 0
        for first in range(radix):
            for second in range(radix):
                if first == second:
                    continue
                if transposition:
                    # Compare the swapped and original two-place contributions.
                    original = first * radix ** (position + 1) + second * radix**position
                    altered = second * radix ** (position + 1) + first * radix**position
                else:
                    original = first * radix**position
                    altered = second * radix**position
                undetected += (altered - original) % modulus == 0
        values.append(undetected)
    return tuple(values)


def test_small_radix_spectra_match_direct_digit_pair_enumeration():
    for radix in (2, 3, 4, 5):
        for modulus in range(2, 9):
            assert radix_substitution_spectrum(radix, modulus, 2) == direct_pair_spectrum(
                radix, modulus, 2, transposition=False
            )
            assert radix_transposition_spectrum(radix, modulus, 2) == direct_pair_spectrum(
                radix, modulus, 2, transposition=True
            )


def test_radix_pair_weight_boundary_values():
    assert radix_pair_weight(11, 1) == 110
    assert radix_pair_weight(11, 10) == 2
    assert radix_pair_weight(11, 11) == 0
    assert radix_pair_weight(11, 12) == 0


def test_radix_stabilization_position():
    assert radix_stabilization_position(10, 14) == 1
    assert radix_stabilization_position(10, 35) == 1
    assert radix_stabilization_position(10, 11) == 0
    assert radix_stabilization_position(2, 512) == 9


def test_enumeration_validates_configuration():
    with pytest.raises(ValueError, match="at least one spectrum"):
        enumerate_radix_spectrum_classes(
            10, 2, 5, 1, include_substitution=False, include_transposition=False
        )
    with pytest.raises(ValueError, match="minimum_modulus"):
        enumerate_radix_spectrum_classes(10, 5, 2, 1)
    with pytest.raises(TypeError, match="include_substitution"):
        enumerate_radix_spectrum_classes(10, 2, 5, 1, include_substitution=1)
