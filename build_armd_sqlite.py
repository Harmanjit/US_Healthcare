"""
One-off ARMD CSV -> SQLite loader (stdlib-only).

What it does
- Reads every *.csv in ../../data/ARMD/
- Creates one SQLite table per CSV (table name derived from filename)
- Stores everything in raw/armd.sqlite (relative to this script)

Why it's fast
- Uses aggressive SQLite bulk-load pragmas (safe enough for a one-time rebuild)
- Inserts in batches inside a single transaction per table
- Minimal type handling: everything is stored as TEXT (simple + reliable)

Run
  python3 build_armd_sqlite.py
  python3 build_armd_sqlite.py --help
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sqlite3
import sys
import time
from pathlib import Path
from typing import Iterable


def _slug_table_name(filename: str) -> str:
    name = Path(filename).stem.lower()
    name = re.sub(r"[^a-z0-9_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        raise ValueError(f"Could not derive table name from {filename!r}")
    if name[0].isdigit():
        name = f"t_{name}"
    return name


def _print_progress(prefix: str, done: int, total: int, *, width: int = 28) -> None:
    if total <= 0:
        return
    frac = min(max(done / total, 0.0), 1.0)
    filled = int(frac * width)
    bar = "#" * filled + "-" * (width - filled)
    # Pad with spaces so shorter updates overwrite previous content cleanly.
    msg = f"\r{prefix} [{bar}] {frac*100:6.2f}%"
    msg = msg[:200].ljust(200)
    sys.stdout.write(msg)
    sys.stdout.flush()


def _iter_csv_rows(path: Path) -> Iterable[list[str]]:
    # newline="" is required for correct CSV handling on all platforms
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            yield row


def _configure_fast_sqlite(conn: sqlite3.Connection) -> None:
    # Wait for locks instead of failing immediately.
    conn.execute("PRAGMA busy_timeout=60000;")  # 60s
    # These settings trade durability for speed during the build.
    conn.execute("PRAGMA journal_mode=OFF;")
    conn.execute("PRAGMA synchronous=OFF;")
    conn.execute("PRAGMA temp_store=MEMORY;")
    conn.execute("PRAGMA locking_mode=EXCLUSIVE;")
    conn.execute("PRAGMA foreign_keys=OFF;")
    # Negative = KiB. ~1GB page cache if memory allows.
    conn.execute("PRAGMA cache_size=-1048576;")
    # Enable memory-mapped I/O where possible (best-effort).
    conn.execute("PRAGMA mmap_size=268435456;")  # 256MB


def _create_table(conn: sqlite3.Connection, table: str, columns: list[str]) -> None:
    # Keep it simple: store all columns as TEXT (works well for one-time loading + exploration).
    cols_sql = ", ".join(f'"{c}" TEXT' for c in columns)
    conn.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({cols_sql});')


def _normalize_columns(raw: list[str]) -> list[str]:
    out: list[str] = []
    used: set[str] = set()
    for i, c in enumerate(raw):
        n = str(c).strip() or f"col_{i+1}"
        n = re.sub(r"\s+", "_", n)
        n = re.sub(r'["`]', "", n)
        n = re.sub(r"[^A-Za-z0-9_]+", "_", n)
        n = re.sub(r"_+", "_", n).strip("_")
        if not n:
            n = f"col_{i+1}"
        # Avoid duplicates by suffixing.
        base = n
        k = 2
        while n in used:
            n = f"{base}__{k}"
            k += 1
        used.add(n)
        out.append(n)
    return out


def load_csv_to_sqlite(
    conn: sqlite3.Connection,
    csv_path: Path,
    table: str,
    *,
    batch_rows: int,
    replace: bool,
) -> None:
    if replace:
        conn.execute(f'DROP TABLE IF EXISTS "{table}";')

    file_size = csv_path.stat().st_size
    t0 = time.time()

    # We read the header first, then stream the rest in batches.
    with csv_path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        # Progress uses the underlying buffered binary position. `f.tell()` can be disabled
        # after iteration via `csv.reader` due to text buffering internals.
        fb = f.buffer
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            print(f"Skipping empty CSV: {csv_path.name}")
            return
        columns = _normalize_columns(header)
        _create_table(conn, table, columns)

        placeholders = ", ".join(["?"] * len(columns))
        col_sql = ", ".join(f'"{c}"' for c in columns)
        insert_sql = f'INSERT INTO "{table}" ({col_sql}) VALUES ({placeholders});'

        batch: list[tuple[str, ...]] = []
        rows_loaded = 0

        # Use byte progress based on underlying file handle position.
        # This is approximate but good enough for a one-off job.
        while True:
            row = next(reader, None)
            if row is None:
                break

            if len(row) != len(columns):
                # Keep shape stable: pad/trim to header length.
                if len(row) < len(columns):
                    row = row + [""] * (len(columns) - len(row))
                else:
                    row = row[: len(columns)]

            batch.append(tuple("" if v is None else str(v) for v in row))
            if len(batch) >= batch_rows:
                conn.executemany(insert_sql, batch)
                rows_loaded += len(batch)
                batch.clear()
                _print_progress(f"{csv_path.name} -> {table}", fb.tell(), file_size)

        if batch:
            conn.executemany(insert_sql, batch)
            rows_loaded += len(batch)
            batch.clear()
            _print_progress(f"{csv_path.name} -> {table}", file_size, file_size)

    elapsed = max(time.time() - t0, 1e-6)
    sys.stdout.write(f"\r{csv_path.name} -> {table} loaded {rows_loaded:,} rows in {elapsed:,.1f}s\n")
    sys.stdout.flush()


def main() -> int:
    parser = argparse.ArgumentParser(description="Load ARMD CSVs into a single SQLite database.")

    # Prefer the user's real dataset location if it exists, otherwise fall back to a relative path.
    default_armd_abs = Path("/Users/harman/Documents/data/ARMD")
    default_armd_rel = (Path(__file__).resolve().parent / ".." / ".." / "data" / "ARMD").resolve()
    default_armd = default_armd_abs if default_armd_abs.exists() else default_armd_rel

    parser.add_argument(
        "--armd-dir",
        default=str(default_armd),
        help=(
            "Folder containing ARMD CSV files. "
            "Defaults to /Users/harman/Documents/data/ARMD if it exists, else ../../data/ARMD."
        ),
    )
    parser.add_argument(
        "--out-db",
        default=str(Path(__file__).resolve().parent / "raw" / "armd.sqlite"),
        help="Output SQLite path (default: raw/armd.sqlite next to this script).",
    )
    parser.add_argument(
        "--batch-rows",
        type=int,
        default=5000,
        help="Rows per insert batch (bigger is faster, uses more RAM).",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Drop/recreate tables if they already exist.",
    )
    args = parser.parse_args()

    armd_dir = Path(os.environ.get("ARMD_DATA_DIR", args.armd_dir)).expanduser().resolve()
    out_db = Path(args.out_db).expanduser().resolve()
    out_db.parent.mkdir(parents=True, exist_ok=True)

    if not armd_dir.exists():
        raise FileNotFoundError(f"ARMD dir not found: {armd_dir}")

    # If we're doing a full rebuild, deleting the file is the simplest/fastest "replace everything".
    # If another process still holds the DB open, you'll get a clear error before we start loading.
    if args.replace and out_db.exists():
        try:
            out_db.unlink()
        except PermissionError as e:
            raise PermissionError(
                f"Could not delete {out_db} (is another loader still running?)"
            ) from e

    csv_files = sorted([p for p in armd_dir.iterdir() if p.is_file() and p.suffix.lower() == ".csv"])
    if not csv_files:
        raise FileNotFoundError(f"No .csv files found in: {armd_dir}")

    print(f"ARMD dir: {armd_dir}")
    print(f"Out DB:   {out_db}")
    print(f"Files:    {len(csv_files)} CSVs\n")

    # Use autocommit off and explicit transactions for speed.
    with sqlite3.connect(out_db, timeout=60.0) as conn:
        _configure_fast_sqlite(conn)

        for i, csv_path in enumerate(csv_files, start=1):
            table = _slug_table_name(csv_path.name)
            print(f"[{i:>3}/{len(csv_files)}] Loading {csv_path.name} -> {table}")
            conn.execute("BEGIN;")
            try:
                load_csv_to_sqlite(
                    conn,
                    csv_path,
                    table,
                    batch_rows=int(args.batch_rows),
                    replace=bool(args.replace),
                )
                conn.execute("COMMIT;")
            except Exception:
                conn.execute("ROLLBACK;")
                raise

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

