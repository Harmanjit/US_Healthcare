import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Paths:
    repo_root: Path
    armd_data_dir: Optional[Path]
    artifacts_dir: Path


def get_paths() -> Paths:
    repo_root = Path(__file__).resolve().parents[2]
    artifacts_dir = (repo_root / "artifacts").resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    armd_env = os.environ.get("ARMD_DATA_DIR")
    armd_data_dir = Path(armd_env).expanduser().resolve() if armd_env else None

    return Paths(repo_root=repo_root, armd_data_dir=armd_data_dir, artifacts_dir=artifacts_dir)

