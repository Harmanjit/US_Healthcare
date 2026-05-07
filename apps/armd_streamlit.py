from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="ARMD Explorer", layout="wide")


def list_tables(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall()
    return [r[0] for r in rows]


def read_table(conn: sqlite3.Connection, table: str, limit: int) -> pd.DataFrame:
    return pd.read_sql_query(f'SELECT * FROM "{table}" LIMIT {int(limit)};', conn)


st.title("ARMD Explorer")

db_default = Path("artifacts/armd.sqlite")
db_path = Path(st.sidebar.text_input("SQLite DB path", str(db_default))).expanduser()
limit = st.sidebar.slider("Rows to preview", min_value=100, max_value=50_000, value=2_000, step=100)

if not db_path.exists():
    st.warning("SQLite DB not found. Build it with: `ehr armd-build-db`")
    st.stop()

with sqlite3.connect(db_path) as conn:
    tables = list_tables(conn)

table = st.sidebar.selectbox("Table", tables, index=tables.index("microbiology_cultures_cohort") if "microbiology_cultures_cohort" in tables else 0)
df = read_table(conn, table, limit=limit)

st.subheader(f"Preview: `{table}` ({len(df):,} rows)")
st.dataframe(df, use_container_width=True, height=450)

st.subheader("Quick chart")
cols = df.columns.tolist()
cat_col = st.selectbox("Column (categorical)", cols, index=cols.index("organism") if "organism" in cols else 0)

vc = (
    df[cat_col]
    .astype(str)
    .fillna("NA")
    .value_counts()
    .head(30)
    .reset_index()
    .rename(columns={"index": cat_col, "count": "count"})
)

fig = px.bar(vc.iloc[::-1], x="count", y=cat_col, orientation="h", height=600)
st.plotly_chart(fig, use_container_width=True)

