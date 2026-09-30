"""Generate common errors in fixed-length decimal strings."""

from collections.abc import Iterator


def _validate_digits(digits: str) -> None:
    """Require a nonempty string containing only decimal digits."""
    if not isinstance(digits, str):
        raise TypeError("digits must be a string")

    if not digits:
        raise ValueError("digits must not be empty")

    if not digits.isascii() or not digits.isdecimal():
        raise ValueError("digits must contain only ASCII decimal digits")


def single_digit_substitutions(digits: str) -> Iterator[str]:
    """Yield strings formed by changing exactly one digit."""
    _validate_digits(digits)

    for position, original in enumerate(digits):
        for replacement in "0123456789":
            if replacement != original:
                yield (
                    digits[:position]
                    + replacement
                    + digits[position + 1:]
                )


def adjacent_transpositions(digits: str) -> Iterator[str]:
    """Yield strings formed by swapping unequal adjacent digits."""
    _validate_digits(digits)

    for position in range(len(digits) - 1):
        if digits[position] == digits[position + 1]:
            continue

        yield (
            digits[:position]
            + digits[position + 1]
            + digits[position]
            + digits[position + 2:]
        )