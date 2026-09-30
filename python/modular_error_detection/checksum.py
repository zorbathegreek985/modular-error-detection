"""Basic modular checksum operations."""


def _validate_value(value: int) -> None:
    """Validate a nonnegative integer, excluding booleans."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an integer (not bool)")
    if value < 0:
        raise ValueError("value must be nonnegative")


def _validate_modulus(modulus: int) -> None:
    """Validate an integer modulus greater than one."""
    if isinstance(modulus, bool) or not isinstance(modulus, int):
        raise TypeError("modulus must be an integer (not bool)")
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")


def checksum(value: int, modulus: int) -> int:
    """Return the least nonnegative residue of value modulo modulus.

    Integer input does not preserve the width of a decimal string.
    For example, the strings "0012" and "12" both represent integer 12.
    """
    _validate_value(value)
    _validate_modulus(modulus)
    return value % modulus


def same_residue(first: int, second: int, modulus: int) -> bool:
    """Return whether two nonnegative integers have equal residues."""
    _validate_value(first)
    _validate_value(second)
    _validate_modulus(modulus)
    return first % modulus == second % modulus
