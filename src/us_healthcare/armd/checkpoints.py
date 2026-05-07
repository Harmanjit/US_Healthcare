from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Checkpoint:
    name: str
    created_at: str
    db_path: str
    table_row_counts: dict[str, int]


class SQLiteCheckpointWriter:
    """
    Creates reproducible "checkpoints" (internal controls) capturing
    row counts per table and build metadata.
    """

    def __init__(self, db_path: Path, out_dir: Path) -> None:
        self.db_path = db_path
        self.out_dir = out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def write(self, name: str) -> Path:
        with sqlite3.connect(self.db_path) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
            ).fetchall()
            table_names = [t[0] for t in tables]
            counts: dict[str, int] = {}
            for t in table_names:
                n = conn.execute(f'SELECT COUNT(1) FROM "{t}";').fetchone()[0]
                counts[t] = int(n)

        cp = Checkpoint(
            name=name,
            created_at=datetime.utcnow().isoformat() + "Z",
            db_path=str(self.db_path),
            table_row_counts=counts,
        )
        path = self.out_dir / f"checkpoint__{name}.json"
        path.write_text(json.dumps(asdict(cp), indent=2, sort_keys=True), encoding="utf-8")
        return path

