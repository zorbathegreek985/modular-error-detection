import pytest

from modular_error_detection.errors import (
    adjacent_transpositions,
    single_digit_substitutions,
)


def test_single_digit_substitutions_count():
    results = list(single_digit_substitutions("12"))
    assert len(results) == 18
    assert len(set(results)) == 18


def test_single_digit_substitutions_change_exactly_one_digit():
    original = "123"
    results = list(single_digit_substitutions(original))

    for result in results:
        assert len(result) == len(original)
        assert sum(a != b for a, b in zip(original, result)) == 1


def test_single_digit_substitutions_preserve_leading_zeros():
    results = list(single_digit_substitutions("001"))

    assert "101" in results
    assert "011" in results
    assert all(len(result) == 3 for result in results)


def test_single_digit_substitutions_can_replace_with_zero():
    results = list(single_digit_substitutions("123"))
    assert "103" in results


def test_adjacent_transpositions():
    results = list(adjacent_transpositions("123"))
    assert results == ["213", "132"]


def test_equal_adjacent_digits_are_skipped():
    results = list(adjacent_transpositions("1123"))
    assert results == ["1213", "1132"]


def test_adjacent_transpositions_preserve_length():
    original = "0123"
    results = list(adjacent_transpositions(original))

    assert all(len(result) == len(original) for result in results)
    assert "1023" in results


def test_single_digit_string_has_no_transpositions():
    assert list(adjacent_transpositions("7")) == []


def test_identical_digits_have_no_transpositions():
    assert list(adjacent_transpositions("1111")) == []


@pytest.mark.parametrize(
    "function",
    [single_digit_substitutions, adjacent_transpositions],
)
@pytest.mark.parametrize("digits", ["", "12a", "１２", "١٢"])
def test_invalid_digit_strings_rejected(function, digits):
    with pytest.raises(ValueError):
        list(function(digits))


@pytest.mark.parametrize(
    "function",
    [single_digit_substitutions, adjacent_transpositions],
)
@pytest.mark.parametrize("digits", [12, None, True])
def test_non_string_inputs_rejected(function, digits):
    with pytest.raises(TypeError):
        list(function(digits))