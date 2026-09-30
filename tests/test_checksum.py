import pytest

from modular_error_detection import checksum, same_residue


@pytest.mark.parametrize(
    ("value", "modulus", "expected"),
    [
        (0, 2, 0),
        (1, 2, 1),
        (10, 3, 1),
        (121, 11, 0),
        (123, 11, 2),
        (999, 10, 9),
    ],
)
def test_checksum_values(value, modulus, expected):
    assert checksum(value, modulus) == expected


def test_checksum_zero():
    assert checksum(0, 11) == 0


def test_checksum_large_integer():
    value = 10**100 + 7
    assert checksum(value, 11) == value % 11


@pytest.mark.parametrize("value", [-1, -100])
def test_negative_value_rejected(value):
    with pytest.raises(ValueError):
        checksum(value, 11)


@pytest.mark.parametrize("value", [1.5, "12", None, True, False])
def test_invalid_value_type_rejected(value):
    with pytest.raises(TypeError):
        checksum(value, 11)


@pytest.mark.parametrize("modulus", [0, 1, -3])
def test_invalid_modulus_rejected(modulus):
    with pytest.raises(ValueError):
        checksum(12, modulus)


@pytest.mark.parametrize("modulus", [2.5, "11", None, True, False])
def test_invalid_modulus_type_rejected(modulus):
    with pytest.raises(TypeError):
        checksum(12, modulus)


def test_same_residue_true():
    assert same_residue(12, 23, 11) is True


def test_same_residue_false():
    assert same_residue(12, 24, 11) is False


def test_same_residue_validates_both_values():
    with pytest.raises(ValueError):
        same_residue(12, -1, 11)
