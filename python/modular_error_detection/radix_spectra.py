"""Bounded radix-generalized modular error-spectrum enumeration.

The spectra use the fixed-width digit model and the substitution and unequal
adjacent-transposition event definitions documented in the research notes.
"""

from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True, slots=True)
class SpectrumClass:
    """Moduli sharing one selected observable spectrum key."""

    representative_modulus: int
    moduli: tuple[int, ...]
    spectrum_key: tuple[int, ...]

    @property
    def size(self) -> int:
        """Number of moduli in this class."""
        return len(self.moduli)


@dataclass(frozen=True, slots=True)
class SpectrumEnumeration:
    """Deterministic result for one bounded radix/modulus domain."""

    radix: int
    minimum_modulus: int
    maximum_modulus: int
    max_position: int
    includes_substitution: bool
    includes_transposition: bool
    moduli_examined: int
    classes: tuple[SpectrumClass, ...]

    @property
    def class_count(self) -> int:
        """Number of distinct observable spectrum keys."""
        return len(self.classes)


def _integer(value: int, name: str, minimum: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer (not bool)")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")


def _validate_domain(radix: int, minimum_modulus: int, maximum_modulus: int) -> None:
    _integer(radix, "radix", 2)
    _integer(minimum_modulus, "minimum_modulus", 2)
    _integer(maximum_modulus, "maximum_modulus", 2)
    if minimum_modulus > maximum_modulus:
        raise ValueError("minimum_modulus must not exceed maximum_modulus")


def radix_pair_weight(radix: int, reduced_divisor: int) -> int:
    """Return ``W_q(h)``: ordered unequal digit pairs with ``h | (a-b)``."""
    _integer(radix, "radix", 2)
    _integer(reduced_divisor, "reduced_divisor", 1)
    return 2 * sum(
        radix - reduced_divisor * multiple
        for multiple in range(1, (radix - 1) // reduced_divisor + 1)
    )


def _reduced_divisor(modulus: int, coefficient: int, radix: int, position: int) -> int:
    return modulus // gcd(modulus, coefficient * radix**position)


def _validate_spectrum_inputs(radix: int, modulus: int, max_position: int) -> None:
    _integer(radix, "radix", 2)
    _integer(modulus, "modulus", 2)
    _integer(max_position, "max_position", 0)


def radix_substitution_spectrum(
    radix: int, modulus: int, max_position: int
) -> tuple[int, ...]:
    """Return ``(S(0), ..., S(max_position))`` for one radix and modulus."""
    _validate_spectrum_inputs(radix, modulus, max_position)
    return tuple(
        radix_pair_weight(
            radix,
            _reduced_divisor(modulus, 1, radix, position),
        )
        for position in range(max_position + 1)
    )


def radix_transposition_spectrum(
    radix: int, modulus: int, max_position: int
) -> tuple[int, ...]:
    """Return ``(T(0), ..., T(max_position))`` for one radix and modulus."""
    _validate_spectrum_inputs(radix, modulus, max_position)
    return tuple(
        radix_pair_weight(
            radix,
            _reduced_divisor(modulus, radix - 1, radix, position),
        )
        for position in range(max_position + 1)
    )


def radix_stabilization_position(radix: int, modulus: int) -> int:
    """Return the first exponent after all radix factors in ``modulus`` cancel.

    This is ``max_p ceil(v_p(modulus) / v_p(radix))`` over primes dividing
    the radix, with value zero when the modulus is coprime to the radix.
    """
    _validate_spectrum_inputs(radix, modulus, 0)
    remaining_radix = radix
    prime_powers: list[tuple[int, int]] = []
    prime = 2
    while prime * prime <= remaining_radix:
        if remaining_radix % prime == 0:
            exponent = 0
            while remaining_radix % prime == 0:
                remaining_radix //= prime
                exponent += 1
            prime_powers.append((prime, exponent))
        prime += 1 if prime == 2 else 2
    if remaining_radix > 1:
        prime_powers.append((remaining_radix, 1))

    required = 0
    for prime, radix_exponent in prime_powers:
        remaining_modulus = modulus
        modulus_exponent = 0
        while remaining_modulus % prime == 0:
            remaining_modulus //= prime
            modulus_exponent += 1
        required = max(
            required,
            (modulus_exponent + radix_exponent - 1) // radix_exponent,
        )
    return required


def enumerate_radix_spectrum_classes(
    radix: int,
    minimum_modulus: int,
    maximum_modulus: int,
    max_position: int,
    *,
    include_substitution: bool = True,
    include_transposition: bool = True,
) -> SpectrumEnumeration:
    """Group moduli by selected spectra over positions ``0..max_position``.

    Keys concatenate the substitution tuple first, when selected, followed by
    the transposition tuple, when selected. The result's selection flags make
    single-spectrum keys unambiguous. A common position endpoint should be at
    least the largest stabilization position in the enumerated domain when
    comparing complete infinite spectra.
    """
    _validate_domain(radix, minimum_modulus, maximum_modulus)
    _integer(max_position, "max_position", 0)
    if not isinstance(include_substitution, bool):
        raise TypeError("include_substitution must be a bool")
    if not isinstance(include_transposition, bool):
        raise TypeError("include_transposition must be a bool")
    if not include_substitution and not include_transposition:
        raise ValueError("at least one spectrum type must be included")

    grouped: dict[tuple[int, ...], list[int]] = {}
    for modulus in range(minimum_modulus, maximum_modulus + 1):
        key_parts: list[int] = []
        if include_substitution:
            key_parts.extend(radix_substitution_spectrum(radix, modulus, max_position))
        if include_transposition:
            key_parts.extend(radix_transposition_spectrum(radix, modulus, max_position))
        grouped.setdefault(tuple(key_parts), []).append(modulus)

    classes = tuple(
        SpectrumClass(
            representative_modulus=moduli[0],
            moduli=tuple(moduli),
            spectrum_key=key,
        )
        for key, moduli in grouped.items()
    )
    return SpectrumEnumeration(
        radix=radix,
        minimum_modulus=minimum_modulus,
        maximum_modulus=maximum_modulus,
        max_position=max_position,
        includes_substitution=include_substitution,
        includes_transposition=include_transposition,
        moduli_examined=maximum_modulus - minimum_modulus + 1,
        classes=classes,
    )
