import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

db_path = sys.argv[1] if len(sys.argv) > 1 else "assistant.db"
folder = Path(__file__).resolve().parents[1] / "sql" / "migrations"
con = sqlite3.connect(db_path)
con.execute("CREATE TABLE IF NOT EXISTS _migrations (name TEXT PRIMARY KEY, applied_at TEXT NOT NULL)")
done = {row[0] for row in con.execute("SELECT name FROM _migrations")}

for f in sorted(folder.glob("*.sql")):
    if f.name in done:
        print(f"skip  {f.name}")
        continue
    with con:  # one transaction per migration
        con.executescript(f.read_text(encoding="utf-8"))
        con.execute("INSERT INTO _migrations VALUES (?, ?)", (f.name, datetime.now(timezone.utc).isoformat()))
    print(f"apply {f.name}")

con.close()