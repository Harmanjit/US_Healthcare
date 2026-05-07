"""
ARMD (Antibiotic Resistance Microbiology Dataset) - data structure understanding.

What this script does:
1) Discovers ARMD CSV files from a configurable data directory.
2) Profiles each table's schema: columns, dtypes, missingness, sample uniqueness.
3) Infers candidate join keys across tables and draws a "table relationship graph".
4) Saves a few high-signal plots that help you *see* the dataset structure.

Usage:
  python armd/armd_data_understanding.py --data-dir "/path/to/ARMD"

Or set:
  export ARMD_DATA_DIR="/path/to/ARMD"
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import pandas as pd


# Ensure plotting caches go to a writable directory.
# This avoids crashes in locked-down environments where ~/.cache isn't writable.
_LOCAL_CACHE_DIR = (Path(__file__).resolve().parent / "_outputs" / "._cache").resolve()
os.environ.setdefault("MPLCONFIGDIR", str((_LOCAL_CACHE_DIR / "matplotlib").resolve()))
os.environ.setdefault("XDG_CACHE_HOME", str((_LOCAL_CACHE_DIR / "xdg").resolve()))
os.environ.setdefault("MPLBACKEND", "Agg")

ARMD_EXPECTED_FILES = [
    "microbiology_cultures_cohort.csv",
    "microbiology_cultures_ward_info.csv",
    "microbiology_cultures_prior_med.csv",
    "microbiology_cultures_microbial_resistance.csv",
    "microbiology_cultures_demographics.csv",
    "microbiology_cultures_labs.csv",
    "microbiology_cultures_vitals.csv",
    "microbiology_cultures_antibiotic_class_exposure.csv",
    "microbiology_cultures_antibiotic_subtype_exposure.csv",
    "microbiology_culture_prior_infecting_organism.csv",
    "microbiology_cultures_comorbidity.csv",
    "microbiology_cultures_priorprocedures.csv",
    "microbiology_cultures_adi_scores.csv",
    "microbiology_cultures_nursing_home_visits.csv",
    "microbiology_cultures_implied_susceptibility.csv",
    "implied_susceptibility_rules.csv",
]

# From the ARMD README "Linking Across Files"
ARMD_LINK_KEYS = [
    "anon_id",  # patient id
    "pat_enc_csn_id_coded",  # encounter id
    "order_proc_id_coded",  # culture order id
    "order_time_jittered_utc",  # jittered timestamp
]


@dataclass(frozen=True)
class ColumnProfile:
    name: str
    dtype: str
    n_missing: int
    missing_frac: float
    n_unique_sample: int
    example_values: list[str]


@dataclass(frozen=True)
class TableProfile:
    table: str
    path: str
    n_rows_sampled: int
    n_cols: int
    columns: list[ColumnProfile]


def _maybe_import_plotting() -> dict[str, Any]:
    """
    Lazy-import plotting libs so the script can still run the profiling even if
    you haven't installed everything yet.
    """
    out: dict[str, Any] = {}
    try:
        import matplotlib.pyplot as plt  # type: ignore

        out["plt"] = plt
    except Exception:
        out["plt"] = None

    try:
        import networkx as nx  # type: ignore

        out["nx"] = nx
    except Exception:
        out["nx"] = None

    return out


def _plot_heatmap_matplotlib(
    df: pd.DataFrame,
    title: str,
    out_png: Path,
    cmap: str = "Blues",
) -> None:
    libs = _maybe_import_plotting()
    plt = libs["plt"]
    if plt is None:
        return

    fig = plt.figure(figsize=(max(10, 1 + df.shape[1] * 1.4), max(8, 0.5 + df.shape[0] * 0.45)))
    ax = fig.add_subplot(1, 1, 1)
    im = ax.imshow(df.values, aspect="auto", cmap=cmap, vmin=float(df.values.min()), vmax=float(df.values.max()))

    ax.set_title(title, fontsize=14)
    ax.set_xticks(range(df.shape[1]))
    ax.set_xticklabels(df.columns.tolist(), rotation=35, ha="right", fontsize=9)
    ax.set_yticks(range(df.shape[0]))
    ax.set_yticklabels(df.index.tolist(), fontsize=9)

    # Light gridlines to separate cells
    ax.set_xticks([x - 0.5 for x in range(1, df.shape[1])], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, df.shape[0])], minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.04)
    cbar.ax.tick_params(labelsize=9)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close(fig)


def resolve_armd_dir(explicit: str | None) -> Path:
    """
    Resolves the ARMD directory.

    Priority:
    - --data-dir
    - ARMD_DATA_DIR env var
    - common relative candidates from repo root
    """
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

    repo_root = Path(__file__).resolve().parents[1]
    candidates = [
        (repo_root / "../../Documents/data/ARMD").resolve(),
        (repo_root / "../../../Documents/data/ARMD").resolve(),
        (repo_root / "../Documents/data/ARMD").resolve(),
        (repo_root / "../../data/ARMD").resolve(),
        (repo_root / "../data/ARMD").resolve(),
    ]
    for p in candidates:
        if p.exists():
            return p

    raise FileNotFoundError(
        "Could not locate ARMD directory. Provide --data-dir or set ARMD_DATA_DIR."
    )


def discover_csvs(armd_dir: Path) -> list[Path]:
    csvs = sorted([p for p in armd_dir.iterdir() if p.suffix.lower() == ".csv"])
    if not csvs:
        raise FileNotFoundError(f"No .csv files found in {armd_dir}")
    return csvs


def _read_csv_sample(path: Path, nrows: int) -> pd.DataFrame:
    # ARMD uses string "null" for missingness in some files (per README).
    return pd.read_csv(
        path,
        nrows=nrows,
        low_memory=False,
        na_values=["null", "NULL", ""],
        keep_default_na=True,
    )


def profile_table(path: Path, nrows: int = 50_000, max_examples: int = 6) -> TableProfile:
    df = _read_csv_sample(path, nrows=nrows)
    cols: list[ColumnProfile] = []
    for c in df.columns:
        s = df[c]
        missing = int(s.isna().sum())
        missing_frac = float(missing / max(len(s), 1))

        # Sample uniqueness (fast). For very wide strings, stringify a small sample.
        nunique = int(s.nunique(dropna=True))
        examples = (
            s.dropna()
            .astype(str)
            .replace("nan", pd.NA)
            .dropna()
            .head(max_examples)
            .tolist()
        )
        cols.append(
            ColumnProfile(
                name=str(c),
                dtype=str(s.dtype),
                n_missing=missing,
                missing_frac=missing_frac,
                n_unique_sample=nunique,
                example_values=[str(x) for x in examples],
            )
        )

    return TableProfile(
        table=path.name,
        path=str(path),
        n_rows_sampled=int(len(df)),
        n_cols=int(df.shape[1]),
        columns=cols,
    )


def build_shared_key_matrix(
    profiles: list[TableProfile],
    keys_of_interest: Iterable[str] = ARMD_LINK_KEYS,
) -> dict[str, dict[str, list[str]]]:
    """
    Returns a mapping: key -> {"present_in": [...tables...], "missing_in": [...tables...]}
    """
    keys = list(keys_of_interest)
    present: dict[str, list[str]] = {k: [] for k in keys}
    missing: dict[str, list[str]] = {k: [] for k in keys}

    for tp in profiles:
        colset = {c.name for c in tp.columns}
        for k in keys:
            (present if k in colset else missing)[k].append(tp.table)

    return {k: {"present_in": present[k], "missing_in": missing[k]} for k in keys}


def infer_join_candidates(profiles: list[TableProfile]) -> dict[str, Any]:
    """
    Heuristic join key inference based on:
    - Known keys from README (ARMD_LINK_KEYS)
    - Column names containing patterns: *_id, id, encounter, order, csn, anon
    - Columns shared across many tables (by exact name)
    """
    table_to_cols = {tp.table: [c.name for c in tp.columns] for tp in profiles}

    # Shared columns across tables
    col_to_tables: dict[str, list[str]] = {}
    for t, cols in table_to_cols.items():
        for c in cols:
            col_to_tables.setdefault(c, []).append(t)

    shared = {
        c: ts for c, ts in col_to_tables.items() if len(ts) >= 2 and c.strip() != ""
    }

    def is_keyish(name: str) -> bool:
        n = name.lower()
        patterns = [
            "anon",
            "patient",
            "enc",
            "csn",
            "order",
            "proc",
            "visit",
            "id",
            "_id",
        ]
        return any(p in n for p in patterns)

    keyish_shared = {c: ts for c, ts in shared.items() if is_keyish(c)}

    return {
        "known_link_keys": ARMD_LINK_KEYS,
        "shared_columns_any": dict(sorted(shared.items(), key=lambda kv: (-len(kv[1]), kv[0]))),
        "shared_columns_keyish": dict(
            sorted(keyish_shared.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        ),
    }


def save_json(obj: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def plot_table_relationship_graph(
    profiles: list[TableProfile],
    join_candidates: dict[str, Any],
    out_png: Path,
) -> None:
    libs = _maybe_import_plotting()
    plt = libs["plt"]
    nx = libs["nx"]
    if plt is None:
        return

    # If networkx is available, draw a nice node-link diagram.
    if nx is not None:
        keyish_shared: dict[str, list[str]] = join_candidates["shared_columns_keyish"]
        G = nx.Graph()

        tables = [tp.table for tp in profiles]
        G.add_nodes_from(tables)

        # Add weighted edges by number of shared keyish columns between table pairs
        pair_weight: dict[tuple[str, str], int] = {}
        for _col, ts in keyish_shared.items():
            ts = sorted(set(ts))
            for i in range(len(ts)):
                for j in range(i + 1, len(ts)):
                    a, b = ts[i], ts[j]
                    pair_weight[(a, b)] = pair_weight.get((a, b), 0) + 1

        for (a, b), w in pair_weight.items():
            G.add_edge(a, b, weight=w)

        if G.number_of_edges() == 0:
            return

        fig = plt.figure(figsize=(14, 10))
        pos = nx.spring_layout(G, seed=7, k=0.7)
        weights = [G[u][v]["weight"] for u, v in G.edges()]
        wmax = max(weights) if weights else 1
        widths = [1.0 + 4.0 * (w / wmax) for w in weights]

        nx.draw_networkx_nodes(G, pos, node_size=1400, node_color="#E6F2FF", edgecolors="#2B5C9A")
        nx.draw_networkx_edges(G, pos, width=widths, alpha=0.7, edge_color="#2B5C9A")
        nx.draw_networkx_labels(G, pos, font_size=8)

        plt.title("ARMD tables: relationship graph (shared key-like columns)", fontsize=14)
        plt.axis("off")
        out_png.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(out_png, dpi=200)
        plt.close(fig)
        return

    # Otherwise, fallback to an adjacency heatmap (no extra dependencies).
    keyish_shared: dict[str, list[str]] = join_candidates["shared_columns_keyish"]
    tables = [tp.table for tp in profiles]
    t_idx = {t: i for i, t in enumerate(tables)}
    mat = [[0 for _ in tables] for _ in tables]
    for _col, ts in keyish_shared.items():
        ts = sorted(set(ts))
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                a, b = ts[i], ts[j]
                ia, ib = t_idx[a], t_idx[b]
                mat[ia][ib] += 1
                mat[ib][ia] += 1

    df = pd.DataFrame(mat, index=tables, columns=tables)
    _plot_heatmap_matplotlib(
        df,
        title="ARMD tables: shared key-like columns (adjacency heatmap)",
        out_png=out_png,
        cmap="Blues",
    )


def plot_key_presence_heatmap(
    profiles: list[TableProfile],
    keys: list[str],
    out_png: Path,
) -> None:
    libs = _maybe_import_plotting()
    plt = libs["plt"]
    if plt is None:
        return

    tables = [tp.table for tp in profiles]
    table_cols = {tp.table: {c.name for c in tp.columns} for tp in profiles}

    data = []
    for t in tables:
        row = [1 if k in table_cols[t] else 0 for k in keys]
        data.append(row)

    df = pd.DataFrame(data, index=tables, columns=keys)
    _plot_heatmap_matplotlib(
        df,
        title="Presence of ARMD linking keys across tables",
        out_png=out_png,
        cmap="Blues",
    )


def plot_top_value_counts(
    armd_dir: Path,
    out_dir: Path,
    sample_rows: int = 200_000,
) -> None:
    """
    High-signal quick plots from the cohort table if present.
    This is intentionally lightweight and uses sampling.
    """
    libs = _maybe_import_plotting()
    plt = libs["plt"]
    if plt is None:
        return

    cohort = armd_dir / "microbiology_cultures_cohort.csv"
    if not cohort.exists():
        return

    df = _read_csv_sample(cohort, nrows=sample_rows)

    # These columns are described in README; only plot those that exist.
    candidate_cols = ["culture_description", "was_positive", "organism", "antibiotic", "susceptibility"]
    present = [c for c in candidate_cols if c in df.columns]
    if not present:
        return

    for c in present:
        vc = df[c].astype(str).fillna("NA").value_counts().head(20)
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(1, 1, 1)
        ax.barh(list(vc.index)[::-1], list(vc.values)[::-1], color="#2B5C9A")
        ax.set_title(f"{cohort.name}: top values for `{c}` (sample n={len(df):,})", fontsize=13)
        ax.set_xlabel("count")
        ax.set_ylabel(c)
        plt.tight_layout()
        out_path = out_dir / f"cohort_top_values__{c}.png"
        plt.savefig(out_path, dpi=200)
        plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description="ARMD: dataset structure understanding + relationship plots.")
    parser.add_argument("--data-dir", default=None, help="Path to ARMD folder containing the CSVs.")
    parser.add_argument("--nrows", type=int, default=50_000, help="Rows to sample per CSV for profiling.")
    parser.add_argument(
        "--out-dir",
        default=str((Path(__file__).resolve().parent / "_outputs").resolve()),
        help="Output directory for reports/plots.",
    )
    args = parser.parse_args()

    armd_dir = resolve_armd_dir(args.data_dir)
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    csvs = discover_csvs(armd_dir)

    # Profile all tables (sampled).
    profiles: list[TableProfile] = []
    for p in csvs:
        profiles.append(profile_table(p, nrows=args.nrows))

    # Relationship inference + reporting.
    key_matrix = build_shared_key_matrix(profiles, keys_of_interest=ARMD_LINK_KEYS)
    join_candidates = infer_join_candidates(profiles)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "armd_dir": str(armd_dir),
        "generated_at": timestamp,
        "expected_files_from_readme": ARMD_EXPECTED_FILES,
        "found_csvs": [p.name for p in csvs],
        "profiles": [asdict(tp) for tp in profiles],
        "key_presence": key_matrix,
        "join_candidates": join_candidates,
    }
    save_json(report, out_dir / f"armd_profile_report__{timestamp}.json")

    # Plots: structure as visuals.
    plot_key_presence_heatmap(profiles, ARMD_LINK_KEYS, out_dir / "key_presence_heatmap.png")
    plot_table_relationship_graph(profiles, join_candidates, out_dir / "table_relationship_graph.png")
    plot_top_value_counts(armd_dir, out_dir)

    # Console summary (kept short by design).
    print(f"ARMD dir: {armd_dir}")
    print(f"Found {len(csvs)} CSVs.")
    print(f"Wrote: {out_dir}")
    print("Key presence (from README link keys):")
    for k, info in key_matrix.items():
        print(f"  - {k}: present in {len(info['present_in'])} tables")
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

