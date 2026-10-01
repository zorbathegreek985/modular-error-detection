from pathlib import Path
import tomllib


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_console_script_points_to_the_cli_main_function():
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as project_file:
        project = tomllib.load(project_file)

    assert project["project"]["scripts"]["financial-data-workbench"] == (
        "financial_data_workbench.cli:main"
    )
