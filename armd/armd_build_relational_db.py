"""
Build a relational SQLite database from the ARMD CSVs.

Design goals:
- One SQLite .db file containing one table per CSV
- Chunked loading for large files
- Minimal dependencies (pandas + stdlib sqlite3)
- OOP structure to keep it extensible for later analyses (EDA, hypothesis tests, etc.)

Usage:
  python3 armd/armd_build_relational_db.py --data-dir "/path/to/ARMD" --out-db "armd/armd.sqlite"

You can also set:
  export ARMD_DATA_DIR="/path/to/ARMD"
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


ARMD_LINK_KEYS = [
    "anon_id",
    "pat_enc_csn_id_coded",
    "order_proc_id_coded",
    "order_time_jittered_utc",
]


def _slug_table_name(csv_filename: str) -> str:
    """
    Convert a CSV filename to a safe SQLite table name.
    """
    name = Path(csv_filename).stem.lower()
    name = re.sub(r"[^a-z0-9_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        raise ValueError(f"Could not derive a table name from: {csv_filename}")
    if name[0].isdigit():
        name = f"t_{name}"
    return name


def _iter_armd_csvs(data_dir: Path) -> list[Path]:
    csvs = sorted([p for p in data_dir.iterdir() if p.is_file() and p.suffix.lower() == ".csv"])
    if not csvs:
        raise FileNotFoundError(f"No CSV files found in {data_dir}")
    return csvs


def _read_csv_chunks(path: Path, chunksize: int) -> Iterable[pd.DataFrame]:
    """
    Stream CSV rows in chunks. ARMD README notes missing values may be the string "null".
    """
    return pd.read_csv(
        path,
        chunksize=chunksize,
        low_memory=False,
        na_values=["null", "NULL", ""],
        keep_default_na=True,
        memory_map=True,
    )


@dataclass(frozen=True)
class BuildConfig:
    data_dir: Path
    out_db: Path
    chunksize: int = 200_000
    if_exists: str = "replace"  # "replace" | "append" | "fail"
    create_indexes: bool = True
    fast_mode: bool = False
    commit_per_table: bool = True


class SQLiteRelationalBuilder:
    """
    Builds and populates a SQLite database from a folder of CSV files.
    """

    def __init__(self, config: BuildConfig) -> None:
        self.config = config
        self.config.out_db.parent.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        csv_paths = _iter_armd_csvs(self.config.data_dir)

        with sqlite3.connect(self.config.out_db) as conn:
            self._configure_connection(conn)

            for csv_path in csv_paths:
                table = _slug_table_name(csv_path.name)
                print(f"Loading {csv_path.name} -> {table} ...", flush=True)
                self._load_csv_to_table(conn, csv_path, table)
                if self.config.create_indexes:
                    self._create_link_key_indexes(conn, table, keys=ARMD_LINK_KEYS)
                print(f"Finished {table}.", flush=True)
                if self.config.commit_per_table:
                    conn.commit()

            self._create_metadata_table(conn, csv_paths)
            conn.commit()

    def _configure_connection(self, conn: sqlite3.Connection) -> None:
        # Pragmas that improve bulk load performance.
        # Note: fast_mode trades durability for speed during the build.
        if self.config.fast_mode:
            conn.execute("PRAGMA journal_mode=MEMORY;")
            conn.execute("PRAGMA synchronous=OFF;")
            conn.execute("PRAGMA temp_store=MEMORY;")
            conn.execute("PRAGMA locking_mode=EXCLUSIVE;")
            # Negative = KiB. ~1GB page cache if memory allows.
            conn.execute("PRAGMA cache_size=-1048576;")
        else:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA temp_store=MEMORY;")

    def _load_csv_to_table(self, conn: sqlite3.Connection, csv_path: Path, table: str) -> None:
        """
        Loads a CSV file into SQLite using pandas.to_sql with chunk iteration.

        Notes:
        - We intentionally don't attempt to enforce strict types up front; ARMD tables are large
          and mixed-type inference across chunks can be tricky. SQLite's dynamic typing works well
          for exploratory analysis.
        """
        first_chunk = True
        t0 = time.time()
        total_rows = 0
        chunk_idx = 0

        for chunk in _read_csv_chunks(csv_path, chunksize=self.config.chunksize):
            chunk_idx += 1
            # Normalize column names slightly to avoid awkward SQL quoting later.
            chunk.columns = [self._normalize_column_name(c) for c in chunk.columns]

            if first_chunk and self.config.if_exists in ("replace", "fail"):
                if self.config.if_exists == "replace":
                    conn.execute(f'DROP TABLE IF EXISTS "{table}";')
                elif self.config.if_exists == "fail":
                    exists = conn.execute(
                        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1;",
                        (table,),
                    ).fetchone()
                    if exists:
                        raise FileExistsError(f"Table already exists and if_exists=fail: {table}")

            chunk.to_sql(
                table,
                conn,
                if_exists="append",
                index=False,
                # Avoid SQLite's "too many SQL variables" by using executemany.
                # With method=None, each row has <= num_columns bound parameters.
                method=None,
                chunksize=50_000 if self.config.fast_mode else 10_000,
            )
            total_rows += int(len(chunk))
            if chunk_idx == 1 or (chunk_idx % 5 == 0):
                elapsed = max(time.time() - t0, 1e-6)
                rate = total_rows / elapsed
                print(
                    f"  - {table}: loaded {total_rows:,} rows in {elapsed:,.1f}s ({rate:,.0f} rows/s)",
                    flush=True,
                )
            first_chunk = False

    def _normalize_column_name(self, name: str) -> str:
        n = str(name).strip()
        n = re.sub(r"\s+", "_", n)
        n = re.sub(r"[^a-zA-Z0-9_]+", "_", n)
        n = re.sub(r"_+", "_", n).strip("_")
        return n

    def _create_link_key_indexes(self, conn: sqlite3.Connection, table: str, keys: list[str]) -> None:
        """
        Creates indexes on any of the known link keys that exist in the table.
        """
        cols = self._get_table_columns(conn, table)
        for key in keys:
            if key in cols:
                idx_name = f"idx__{table}__{key}"
                conn.execute(f'CREATE INDEX IF NOT EXISTS "{idx_name}" ON "{table}"("{key}");')

    def _get_table_columns(self, conn: sqlite3.Connection, table: str) -> set[str]:
        rows = conn.execute(f'PRAGMA table_info("{table}");').fetchall()
        # PRAGMA table_info: (cid, name, type, notnull, dflt_value, pk)
        return {r[1] for r in rows}

    def _create_metadata_table(self, conn: sqlite3.Connection, csv_paths: list[Path]) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS armd__source_files (
              csv_filename TEXT PRIMARY KEY,
              table_name TEXT NOT NULL,
              csv_path TEXT NOT NULL
            );
            """
        )
        for p in csv_paths:
            conn.execute(
                """
                INSERT OR REPLACE INTO armd__source_files (csv_filename, table_name, csv_path)
                VALUES (?, ?, ?);
                """,
                (p.name, _slug_table_name(p.name), str(p)),
            )


def resolve_armd_dir(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if p.exists():
            return p
        raise FileNotFoundError(f"--data-dir not found: {p}")

    env = os.environ.get("ARMD_DATA_DIR")
    if env:
        p = Path(env).expanduser().resolve()
        if p.exists():
            return p
        raise FileNotFoundError(f"ARMD_DATA_DIR not found: {p}")

    raise FileNotFoundError("Provide --data-dir or set ARMD_DATA_DIR.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SQLite DB from ARMD CSVs.")
    parser.add_argument("--data-dir", default=None, help="Path to ARMD folder containing the CSVs.")
    parser.add_argument(
        "--out-db",
        default="armd/armd.sqlite",
        help="Output SQLite database path (relative to repo root if not absolute).",
    )
    parser.add_argument("--chunksize", type=int, default=200_000, help="Rows per chunk while loading CSVs.")
    parser.add_argument(
        "--if-exists",
        default="replace",
        choices=["replace", "append", "fail"],
        help="What to do if tables already exist.",
    )
    parser.add_argument(
        "--no-indexes",
        action="store_true",
        help="Skip creating indexes on linking keys (faster load, slower joins).",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Faster build (less durable pragmas, bigger insert batches). Recommended for initial DB creation.",
    )
    args = parser.parse_args()

    data_dir = resolve_armd_dir(args.data_dir)
    out_db = Path(args.out_db).expanduser()
    if not out_db.is_absolute():
        repo_root = Path(__file__).resolve().parents[1]
        out_db = (repo_root / out_db).resolve()

    config = BuildConfig(
        data_dir=data_dir,
        out_db=out_db,
        chunksize=int(args.chunksize),
        if_exists=str(args.if_exists),
        create_indexes=not bool(args.no_indexes),
        fast_mode=bool(args.fast),
    )
    builder = SQLiteRelationalBuilder(config)
    builder.run()

    print(f"Wrote SQLite DB: {config.out_db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

