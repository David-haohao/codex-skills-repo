import argparse
import re
import sys
from typing import Iterable, List, Optional

import pymysql


HOST = "172.18.1.31"
PORT = 9030
USER = "ctoken"
PASSWORD = "ctoken@qwer#2025"
DEFAULT_DB = "ods_credit_core"


def _extract_table_candidates(sql: str) -> List[str]:
    # Match simple FROM/JOIN targets; keep only bare table names.
    pattern = re.compile(r"\b(?:from|join)\s+([a-zA-Z0-9_\.]+)", re.IGNORECASE)
    tables: List[str] = []
    for raw in pattern.findall(sql):
        name = raw.strip().strip("`")
        if "." in name:
            name = name.split(".")[-1]
        if name and name.lower() not in ("select",):
            tables.append(name)
    # Deduplicate preserving order.
    seen = set()
    ordered = []
    for t in tables:
        if t not in seen:
            ordered.append(t)
            seen.add(t)
    return ordered


def _query_table_schema(conn, table_name: str) -> List[str]:
    sql = """
select
    table_schema
from information_schema.tables
where table_name = %s
order by table_schema
"""
    with conn.cursor() as cur:
        cur.execute(sql, (table_name,))
        return [r[0] for r in cur.fetchall()]


def _resolve_database(
    table_names: Iterable[str], forced_db: Optional[str] = None
) -> Optional[str]:
    if forced_db:
        return forced_db
    table_names = list(table_names)
    if not table_names:
        return DEFAULT_DB

    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database="information_schema",
        connect_timeout=10,
        read_timeout=30,
        write_timeout=30,
        charset="utf8mb4",
    )
    try:
        schema_sets = []
        for name in table_names:
            schemas = _query_table_schema(conn, name)
            if not schemas:
                raise RuntimeError(f"Table not found in information_schema: {name}")
            schema_sets.append(set(schemas))
        intersection = set.intersection(*schema_sets)
        if not intersection:
            raise RuntimeError(
                f"Could not resolve one common database for tables: {', '.join(table_names)}"
            )
        if DEFAULT_DB in intersection:
            return DEFAULT_DB
        return sorted(intersection)[0]
    finally:
        conn.close()


def _print_rows(rows):
    for row in rows:
        print("\t".join("" if v is None else str(v) for v in row))


def main():
    parser = argparse.ArgumentParser(
        description="Execute SQL via pymysql with table-schema precheck."
    )
    parser.add_argument("--sql-file", help="Path to SQL file.")
    parser.add_argument("--database", help="Force database, skip auto resolve.")
    parser.add_argument(
        "--limit-output",
        type=int,
        default=200,
        help="Max output rows printed to console.",
    )
    args = parser.parse_args()

    if args.sql_file:
        with open(args.sql_file, "r", encoding="utf-8-sig") as f:
            sql = f.read().lstrip("\ufeff").strip()
    else:
        sql = sys.stdin.read().lstrip("\ufeff").strip()

    if not sql:
        raise RuntimeError("Empty SQL input.")

    table_names = _extract_table_candidates(sql)
    db = _resolve_database(table_names, args.database)
    print(f"[INFO] resolved_database={db}")
    if table_names:
        print(f"[INFO] table_candidates={','.join(table_names)}")

    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=db,
        connect_timeout=10,
        read_timeout=120,
        write_timeout=120,
        charset="utf8mb4",
    )
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            print(f"[INFO] row_count={len(rows)}")
            _print_rows(rows[: args.limit_output])
    finally:
        conn.close()


if __name__ == "__main__":
    main()

