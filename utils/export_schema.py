from pathlib import Path
import sqlite3


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    db_path = project_root / "db.sqlite3"
    out_path = Path(__file__).resolve().parent / "schema_full.sql"

    if not db_path.exists():
        raise FileNotFoundError(f"No se encontro la base de datos: {db_path}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    rows = cur.execute(
        """
        SELECT type, name, sql
        FROM sqlite_master
        WHERE sql IS NOT NULL
          AND type IN ('table', 'index', 'trigger', 'view')
          AND name NOT LIKE 'sqlite_%'
        ORDER BY
          CASE type
            WHEN 'table' THEN 1
            WHEN 'index' THEN 2
            WHEN 'trigger' THEN 3
            ELSE 4
          END,
          name;
        """
    ).fetchall()

    with out_path.open("w", encoding="utf-8", newline="\n") as file:
        file.write("PRAGMA foreign_keys = OFF;\n")
        file.write("BEGIN TRANSACTION;\n\n")

        for _obj_type, _name, sql in rows:
            file.write(sql.rstrip() + ";\n\n")

        file.write("COMMIT;\n")
        file.write("PRAGMA foreign_keys = ON;\n")

    conn.close()
    print(f"SQL generado en: {out_path}")


if __name__ == "__main__":
    main()
