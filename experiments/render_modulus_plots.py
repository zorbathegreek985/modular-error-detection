"""Render separate SVG detection-rate plots from the sweep CSV."""

from pathlib import Path

from modular_error_detection.visualizations import write_detection_plot

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "reports" / "modulus_sweep.csv"
PLOT_PATHS = {
    "substitution": ROOT / "reports" / "substitution_detection_rate.svg",
    "transposition": ROOT / "reports" / "transposition_detection_rate.svg",
}


def main() -> None:
    for error_type, output_path in PLOT_PATHS.items():
        points = write_detection_plot(CSV_PATH, output_path, error_type)
        print(f"Generated: {output_path} ({len(points)} moduli)")


if __name__ == "__main__":
    main()
