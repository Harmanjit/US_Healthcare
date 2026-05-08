"""
Compact ARMD SQLite explorer (stdlib-only, OOP).

What you get (per table)
- row count
- schema (column names)
- a small random-ish sample (first N rows)
- per-column: null/empty count and distinct count (limited to a max columns)

Run
  python3 -B explore_armd_sqlite.py
  python3 -B explore_armd_sqlite.py --help
"""

from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ColumnStat:
    name: str
    null_or_empty: int
    distinct: int


class SQLiteExplorer:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def connect(self) -> sqlite3.Connection:
        if not self.db_path.exists():
            raise FileNotFoundError(f"DB not found: {self.db_path}")
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def list_tables(self, conn: sqlite3.Connection) -> list[str]:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
        ).fetchall()
        return [r[0] for r in rows]

    def table_columns(self, conn: sqlite3.Connection, table: str) -> list[str]:
        rows = conn.execute(f'PRAGMA table_info("{table}");').fetchall()
        return [r[1] for r in rows]  # (cid, name, type, notnull, dflt_value, pk)

    def row_count(self, conn: sqlite3.Connection, table: str) -> int:
        return int(conn.execute(f'SELECT COUNT(1) FROM "{table}";').fetchone()[0])

    def sample_rows(self, conn: sqlite3.Connection, table: str, limit: int) -> list[sqlite3.Row]:
        return conn.execute(f'SELECT * FROM "{table}" LIMIT {int(limit)};').fetchall()

    def column_stats(self, conn: sqlite3.Connection, table: str, col: str) -> ColumnStat:
        # Loader stores TEXT. Treat NULL and "" as missing.
        q = f"""
        SELECT
          SUM(CASE WHEN "{col}" IS NULL OR "{col}" = '' THEN 1 ELSE 0 END) AS null_or_empty,
          COUNT(DISTINCT "{col}") AS distinct_count
        FROM "{table}";
        """
        row = conn.execute(q).fetchone()
        return ColumnStat(name=col, null_or_empty=int(row[0] or 0), distinct=int(row[1] or 0))


def _fmt_int(n: int) -> str:
    return f"{n:,}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Explore an ARMD SQLite DB.")
    parser.add_argument(
        "--db",
        default=str(Path(__file__).resolve().parent / "raw" / "armd.sqlite"),
        help="Path to SQLite DB (default: raw/armd.sqlite).",
    )
    parser.add_argument("--sample-rows", type=int, default=5, help="Rows to preview per table.")
    parser.add_argument(
        "--max-stat-cols",
        type=int,
        default=25,
        help="Max columns per table to compute stats for (keeps it fast).",
    )
    args = parser.parse_args()

    explorer = SQLiteExplorer(Path(args.db).expanduser().resolve())
    with explorer.connect() as conn:
        tables = explorer.list_tables(conn)
        print(f"DB: {explorer.db_path}")
        print(f"Tables: {len(tables)}\n")

        for t in tables:
            cols = explorer.table_columns(conn, t)
            n = explorer.row_count(conn, t)
            print("=" * 88)
            print(f"TABLE: {t}")
            print(f"Rows:  {_fmt_int(n)}")
            print(f"Cols:  {len(cols)}")
            print(f"Schema: {', '.join(cols[:12])}{' ...' if len(cols) > 12 else ''}\n")

            # Column stats (limited)
            stat_cols = cols[: max(0, int(args.max_stat_cols))]
            if stat_cols:
                print("Column stats (null/empty, distinct):")
                for c in stat_cols:
                    s = explorer.column_stats(conn, t, c)
                    print(f"- {s.name}: null/empty={_fmt_int(s.null_or_empty)} distinct={_fmt_int(s.distinct)}")
                if len(cols) > len(stat_cols):
                    print(f"(skipped {len(cols) - len(stat_cols)} columns; use --max-stat-cols to change)\n")
                else:
                    print()

            # Sample
            sample = explorer.sample_rows(conn, t, limit=int(args.sample_rows))
            if not sample:
                print("Sample: (no rows)")
                continue

            sample_cols = cols[: min(8, len(cols))]
            print(f"Sample (first {len(sample)} rows; showing up to {len(sample_cols)} cols):")
            for i, r in enumerate(sample, start=1):
                bits = []
                for c in sample_cols:
                    v = r[c]
                    s = "" if v is None else str(v)
                    if len(s) > 60:
                        s = s[:57] + "..."
                    bits.append(f"{c}={s!r}")
                print(f"- row {i}: " + ", ".join(bits))
            print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

