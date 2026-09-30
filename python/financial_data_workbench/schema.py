"""Configuration objects for financial CSV validation.

Numeric constraints use decimal values and never convert through ``float``.
Timestamp cadence is a simple elapsed-time interval. It does not model an
exchange calendar, market sessions, holidays, or daylight-saving schedules.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from types import MappingProxyType
from typing import Mapping


SupportedColumnType = type
_SUPPORTED_TYPES = {str, int, Decimal, bool, date, datetime}


def _decimal_bound(value: Decimal | int | str | None, name: str) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(f"{name} must be a Decimal, integer, or decimal string")
    try:
        result = value if isinstance(value, Decimal) else Decimal(value)
    except (InvalidOperation, TypeError, ValueError) as error:
        raise ValueError(f"{name} must be a finite decimal value") from error
    if not result.is_finite():
        raise ValueError(f"{name} must be finite")
    return result


@dataclass(frozen=True)
class NumericConstraint:
    """Optional inclusive/exclusive bounds for a decimal-valued column."""

    minimum: Decimal | int | str | None = None
    maximum: Decimal | int | str | None = None
    minimum_inclusive: bool = True
    maximum_inclusive: bool = True

    def __post_init__(self) -> None:
        if type(self.minimum_inclusive) is not bool:
            raise TypeError("minimum_inclusive must be a bool")
        if type(self.maximum_inclusive) is not bool:
            raise TypeError("maximum_inclusive must be a bool")
        minimum = _decimal_bound(self.minimum, "minimum")
        maximum = _decimal_bound(self.maximum, "maximum")
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError("minimum must not exceed maximum")
        if (minimum is not None and maximum is not None and minimum == maximum
                and not (self.minimum_inclusive and self.maximum_inclusive)):
            raise ValueError("equal bounds require both bounds to be inclusive")
        object.__setattr__(self, "minimum", minimum)
        object.__setattr__(self, "maximum", maximum)


@dataclass(frozen=True)
class OHLCColumns:
    """Names of configured OHLC columns and an optional volume column."""

    open: str = "Open"
    high: str = "High"
    low: str = "Low"
    close: str = "Close"
    volume: str | None = "Volume"

    def __post_init__(self) -> None:
        for name in ("open", "high", "low", "close"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} column name must be a nonempty string")
        if self.volume is not None and (
            not isinstance(self.volume, str) or not self.volume.strip()
        ):
            raise ValueError("volume column name must be None or a nonempty string")

    @property
    def price_columns(self) -> tuple[str, str, str, str]:
        return self.open, self.high, self.low, self.close

    @property
    def all_columns(self) -> tuple[str, ...]:
        return self.price_columns + ((self.volume,) if self.volume else ())


@dataclass(frozen=True)
class DataSchema:
    """Describe required fields and opt-in validation rules for one dataset.

    ``column_types`` supports ``str``, ``int``, ``Decimal``, ``bool``,
    ``date``, and ``datetime``. ``float`` is intentionally unsupported for
    financial numeric validation; use ``Decimal`` instead. A value containing
    only whitespace is considered missing. Nonempty source values are retained
    verbatim by the loader; surrounding whitespace is stripped only when a
    validator parses a value.
    """

    required_columns: tuple[str, ...]
    column_types: Mapping[str, SupportedColumnType] = field(default_factory=dict)
    timestamp_column: str | None = None
    expected_cadence: timedelta | None = None
    numeric_constraints: Mapping[str, NumericConstraint] = field(default_factory=dict)
    ohlc_columns: OHLCColumns | None = None

    def __post_init__(self) -> None:
        if isinstance(self.required_columns, str):
            raise TypeError("required_columns must be a sequence of column names")
        required = tuple(self.required_columns)
        if any(not isinstance(name, str) or not name.strip() for name in required):
            raise ValueError("required column names must be nonempty strings")
        if len(required) != len(set(required)):
            raise ValueError("required column names must be unique")
        object.__setattr__(self, "required_columns", required)

        types = dict(self.column_types)
        for column, kind in types.items():
            if column not in required:
                raise ValueError(f"typed column {column!r} must be required")
            if kind not in _SUPPORTED_TYPES:
                raise TypeError(f"unsupported type for column {column!r}: {kind!r}")
        object.__setattr__(self, "column_types", MappingProxyType(types))

        constraints = dict(self.numeric_constraints)
        for column, constraint in constraints.items():
            if column not in required:
                raise ValueError(f"constrained column {column!r} must be required")
            if not isinstance(constraint, NumericConstraint):
                raise TypeError(f"constraint for {column!r} must be NumericConstraint")
        object.__setattr__(self, "numeric_constraints", MappingProxyType(constraints))

        if self.timestamp_column is not None and self.timestamp_column not in required:
            raise ValueError("timestamp_column must be included in required_columns")
        if (self.timestamp_column is not None
                and self.column_types.get(self.timestamp_column) not in {None, datetime}):
            raise ValueError("timestamp_column must use datetime validation")
        if self.expected_cadence is not None:
            if not isinstance(self.expected_cadence, timedelta):
                raise TypeError("expected_cadence must be a timedelta")
            if self.expected_cadence <= timedelta(0):
                raise ValueError("expected_cadence must be positive")
            if self.timestamp_column is None:
                raise ValueError("expected_cadence requires a timestamp_column")

        if self.ohlc_columns is not None and not isinstance(self.ohlc_columns, OHLCColumns):
            raise TypeError("ohlc_columns must be None or an OHLCColumns instance")
        if self.ohlc_columns is not None:
            names = self.ohlc_columns.all_columns
            if len(names) != len(set(names)):
                raise ValueError("OHLCV column names must be distinct")
            missing = set(names) - set(required)
            if missing:
                raise ValueError(
                    "configured OHLCV columns must be required: "
                    + ", ".join(sorted(missing))
                )
