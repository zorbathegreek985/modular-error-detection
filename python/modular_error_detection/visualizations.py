"""Prepare and render SVG visualizations from sweep CSV data."""

import csv
from collections import defaultdict
from html import escape
from pathlib import Path


def aggregate_detection_rates(
    csv_path: Path, error_type: str
) -> list[tuple[int, float | None]]:
    """Return event-weighted detection rates by modulus.

    Rows with no events contribute no observations. A modulus with no
    events across all of its rows is represented by ``None``.
    """
    if error_type not in {"substitution", "transposition"}:
        raise ValueError("unknown error type")

    counts: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    with Path(csv_path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required = {
            "modulus", "error_type", "total_events", "detected_events"
        }
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("CSV is missing required sweep columns")

        for row in reader:
            if row["error_type"] != error_type:
                continue
            try:
                modulus = int(row["modulus"])
                total = int(row["total_events"])
                detected = int(row["detected_events"])
            except (TypeError, ValueError) as error:
                raise ValueError("CSV contains invalid event counts") from error
            if modulus <= 1 or total < 0 or detected < 0 or detected > total:
                raise ValueError("CSV contains out-of-range event counts")
            counts[modulus][0] += total
            counts[modulus][1] += detected

    return [
        (modulus, detected / total if total else None)
        for modulus, (total, detected) in sorted(counts.items())
    ]


def _render_svg(
    points: list[tuple[int, float | None]], title: str, error_label: str
) -> str:
    width, height = 1200, 720
    left, right, top, bottom = 105, 35, 105, 105
    plot_width = width - left - right
    plot_height = height - top - bottom
    min_modulus = min(modulus for modulus, _ in points)
    max_modulus = max(modulus for modulus, _ in points)

    def x_position(modulus: int) -> float:
        span = max_modulus - min_modulus
        return left + (modulus - min_modulus) / span * plot_width if span else left + plot_width / 2

    def y_position(rate: float) -> float:
        return top + (1 - rate) * plot_height

    items = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<g font-family="Segoe UI, Arial, sans-serif" fill="#172033">',
        f'<text x="{width / 2:g}" y="42" text-anchor="middle" font-size="27" font-weight="700">{escape(title)}</text>',
        f'<text x="{width / 2:g}" y="73" text-anchor="middle" font-size="16" fill="#536174">Moduli {min_modulus}–{max_modulus} · string lengths 1–4 · event-weighted across lengths</text>',
    ]

    for percent in range(0, 101, 10):
        y = y_position(percent / 100)
        items.append(f'<line x1="{left}" y1="{y:.2f}" x2="{width-right}" y2="{y:.2f}" stroke="#dce3ec" stroke-width="1"/>')
        items.append(f'<text x="{left-14}" y="{y+5:.2f}" text-anchor="end" font-size="14" fill="#536174">{percent}%</text>')

    ticks = list(range(min_modulus, max_modulus + 1, 2))
    if ticks[-1] != max_modulus:
        ticks.append(max_modulus)
    for modulus in ticks:
        x = x_position(modulus)
        items.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{height-bottom}" stroke="#eef1f5" stroke-width="1"/>')
        items.append(f'<text x="{x:.2f}" y="{height-bottom+25}" text-anchor="middle" font-size="14" fill="#536174">{modulus}</text>')

    items.extend([
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#667085" stroke-width="1.5"/>',
        f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#667085" stroke-width="1.5"/>',
        f'<text x="{width/2:g}" y="{height-28}" text-anchor="middle" font-size="17" font-weight="600">Modulus</text>',
        f'<text x="28" y="{height/2:g}" text-anchor="middle" font-size="17" font-weight="600" transform="rotate(-90 28 {height/2:g})">Detection rate</text>',
    ])

    # Break the line at missing aggregate rates rather than treating them as 0%.
    segments: list[list[tuple[float, float]]] = []
    segment: list[tuple[float, float]] = []
    for modulus, rate in points:
        if rate is None:
            if segment:
                segments.append(segment)
                segment = []
            continue
        segment.append((x_position(modulus), y_position(rate)))
    if segment:
        segments.append(segment)

    color = "#2563eb" if error_label == "substitution" else "#c2410c"
    for series in segments:
        if len(series) > 1:
            coordinates = " ".join(f"{x:.2f},{y:.2f}" for x, y in series)
            items.append(f'<polyline points="{coordinates}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
        for x, y in series:
            items.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.5" fill="{color}" stroke="#ffffff" stroke-width="1.5"/>')

    if any(rate is None for _, rate in points):
        items.append(f'<text x="{width-right}" y="{top+22}" text-anchor="end" font-size="13" fill="#8a4b08">N/A values omitted from the line</text>')
    items.append('</g></svg>')
    return "\n".join(items) + "\n"


def write_detection_plot(
    csv_path: Path, output_path: Path, error_type: str
) -> list[tuple[int, float | None]]:
    """Aggregate CSV counts, write a percentage-rate SVG, and return its data."""
    labels = {
        "substitution": ("Single-digit substitution detection rate by modulus", "substitution"),
        "transposition": ("Unequal adjacent-transposition detection rate by modulus", "transposition"),
    }
    if error_type not in labels:
        raise ValueError("unknown error type")
    points = aggregate_detection_rates(csv_path, error_type)
    if not points:
        raise ValueError(f"CSV contains no rows for {error_type}")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(_render_svg(points, *labels[error_type]), encoding="utf-8")
    return points
