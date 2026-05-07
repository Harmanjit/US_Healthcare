from pathlib import Path
from typing import Optional

import typer
from rich import print

from us_healthcare.config import get_paths

app = typer.Typer(help="EHR analytics utilities (ARMD-first).")


@app.command()
def info() -> None:
    """Print resolved paths and environment configuration."""
    paths = get_paths()
    print("[bold]Repo root:[/bold]", paths.repo_root)
    print("[bold]Artifacts dir:[/bold]", paths.artifacts_dir)
    print("[bold]ARMD_DATA_DIR:[/bold]", paths.armd_data_dir)


@app.command()
def armd_profile(
    data_dir: Optional[Path] = typer.Option(
        None, help="Path to ARMD folder (overrides ARMD_DATA_DIR)."
    ),
    nrows: int = typer.Option(50_000, help="Rows to sample per CSV for profiling."),
) -> None:
    """
    Run the existing ARMD structure profiler (writes plots + JSON report).

    This calls the script in `armd/armd_data_understanding.py` to keep behavior identical.
    """
    from subprocess import run

    paths = get_paths()
    resolved = data_dir or paths.armd_data_dir
    if resolved is None:
        raise typer.BadParameter("Provide --data-dir or set ARMD_DATA_DIR.")

    cmd = [
        "python3",
        str((paths.repo_root / "armd" / "armd_data_understanding.py").resolve()),
        "--data-dir",
        str(resolved),
        "--nrows",
        str(nrows),
    ]
    print("[bold]Running:[/bold]", " ".join(cmd))
    raise SystemExit(run(cmd).returncode)


@app.command()
def armd_build_db(
    data_dir: Optional[Path] = typer.Option(
        None, help="Path to ARMD folder (overrides ARMD_DATA_DIR)."
    ),
    out_db: Path = typer.Option(Path("artifacts/armd.sqlite"), help="Output SQLite file."),
    chunksize: int = typer.Option(200_000, help="Rows per CSV chunk while loading."),
    fast: bool = typer.Option(True, help="Use fast bulk-load pragmas."),
    no_indexes: bool = typer.Option(True, help="Skip indexes during initial build."),
) -> None:
    """
    Build an ARMD SQLite database (one table per CSV).
    """
    from subprocess import run

    paths = get_paths()
    resolved = data_dir or paths.armd_data_dir
    if resolved is None:
        raise typer.BadParameter("Provide --data-dir or set ARMD_DATA_DIR.")

    cmd = [
        "python3",
        "-u",
        str((paths.repo_root / "armd" / "armd_build_relational_db.py").resolve()),
        "--data-dir",
        str(resolved),
        "--out-db",
        str((paths.repo_root / out_db).resolve() if not out_db.is_absolute() else out_db),
        "--chunksize",
        str(chunksize),
        "--if-exists",
        "replace",
    ]
    if fast:
        cmd.append("--fast")
    if no_indexes:
        cmd.append("--no-indexes")

    print("[bold]Running:[/bold]", " ".join(cmd))
    raise SystemExit(run(cmd).returncode)


@app.command()
def armd_validate(
    db: Path = typer.Option(Path("artifacts/armd.sqlite"), help="Path to ARMD sqlite db."),
) -> None:
    """Run internal validation checks against the ARMD SQLite database."""
    from us_healthcare.armd.validate import ARMDValidator

    paths = get_paths()
    db_path = (paths.repo_root / db).resolve() if not db.is_absolute() else db
    results = ARMDValidator(db_path).run()
    for r in results:
        status = "[green]OK[/green]" if r.ok else "[red]FAIL[/red]"
        print(f"{status} {r.message}")
    if any(not r.ok for r in results):
        raise SystemExit(1)


@app.command()
def armd_checkpoint(
    name: str = typer.Option(..., help="Checkpoint name, e.g. v1_initial_build."),
    db: Path = typer.Option(Path("artifacts/armd.sqlite"), help="Path to ARMD sqlite db."),
    out_dir: Path = typer.Option(Path("artifacts/checkpoints"), help="Where to write checkpoint JSON."),
) -> None:
    """Write a checkpoint JSON capturing table row counts."""
    from us_healthcare.armd.checkpoints import SQLiteCheckpointWriter

    paths = get_paths()
    db_path = (paths.repo_root / db).resolve() if not db.is_absolute() else db
    out = (paths.repo_root / out_dir).resolve() if not out_dir.is_absolute() else out_dir
    p = SQLiteCheckpointWriter(db_path, out).write(name=name)
    print("[bold]Wrote checkpoint:[/bold]", p)


if __name__ == "__main__":
    app()

