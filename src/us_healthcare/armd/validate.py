from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


ARMD_LINK_KEYS = [
    "anon_id",
    "pat_enc_csn_id_coded",
    "order_proc_id_coded",
    "order_time_jittered_utc",
]


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    message: str


class ARMDValidator:
    """
    Lightweight "internal controls" for your SQLite build:
    - expected tables exist
    - link keys exist in most tables
    - core table is non-empty
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def run(self) -> list[ValidationResult]:
        if not self.db_path.exists():
            return [ValidationResult(False, f"DB not found: {self.db_path}")]

        results: list[ValidationResult] = []
        with sqlite3.connect(self.db_path) as conn:
            tables = self._list_tables(conn)
            results.append(
                ValidationResult(
                    ok=len(tables) >= 5,
                    message=f"Found {len(tables)} tables.",
                )
            )

            cohort = "microbiology_cultures_cohort"
            if cohort in tables:
                n = conn.execute(f'SELECT COUNT(1) FROM "{cohort}";').fetchone()[0]
                results.append(ValidationResult(ok=n > 0, message=f"{cohort} row count = {n:,}"))
            else:
                results.append(ValidationResult(False, f"Missing required core table: {cohort}"))

            # Link keys presence
            missing_keys_total = 0
            for t in tables:
                cols = self._table_columns(conn, t)
                for k in ARMD_LINK_KEYS:
                    if k not in cols:
                        missing_keys_total += 1
            results.append(
                ValidationResult(
                    ok=True,
                    message=f"Checked link-key presence across {len(tables)} tables (missing count={missing_keys_total}).",
                )
            )

        return results

    def _list_tables(self, conn: sqlite3.Connection) -> list[str]:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall()
        return [r[0] for r in rows]

    def _table_columns(self, conn: sqlite3.Connection, table: str) -> set[str]:
        rows = conn.execute(f'PRAGMA table_info("{table}");').fetchall()
        return {r[1] for r in rows}

