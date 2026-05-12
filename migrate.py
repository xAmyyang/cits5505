import sqlite3
from pathlib import Path

DB_PATH = "instance/survivechef.db"
MIGRATIONS_DIR = Path("migrations")


def get_current_version(db):
    db.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY
        )
    """)

    row = db.execute("""
        SELECT MAX(version) FROM schema_migrations
    """).fetchone()

    return row[0] if row[0] is not None else 0


def run_sql_file(db, path):
    sql = path.read_text(encoding="utf-8")
    db.executescript(sql)


def upgrade():
    conn = sqlite3.connect(DB_PATH)
    db = conn.cursor()

    current = get_current_version(db)

    files = sorted(MIGRATIONS_DIR.glob("*_up.sql"))

    for file in files:
        version = int(file.name.split("_")[0])

        if version == current + 1:
            print(f"Running {file.name}")
            run_sql_file(db, file)
            db.execute(
                "INSERT INTO schema_migrations (version) VALUES (?)",
                (version,)
            )
            conn.commit()
            print(f"Upgraded to version {version}")
            conn.close()
            return

    print("Already up to date.")
    conn.close()


def downgrade():
    conn = sqlite3.connect(DB_PATH)
    db = conn.cursor()

    current = get_current_version(db)

    if current == 0:
        print("Already at version 0.")
        conn.close()
        return

    down_file = MIGRATIONS_DIR / f"{current:03d}_down.sql"

    if not down_file.exists():
        print(f"No downgrade file found: {down_file}")
        conn.close()
        return

    print(f"Running {down_file.name}")
    run_sql_file(db, down_file)

    db.execute(
        "DELETE FROM schema_migrations WHERE version = ?",
        (current,)
    )

    conn.commit()
    conn.close()
    print(f"Downgraded to version {current - 1}")


if __name__ == "__main__":
    import sys

    command = sys.argv[1] if len(sys.argv) > 1 else "upgrade"

    if command == "upgrade":
        upgrade()
    elif command == "downgrade":
        downgrade()
    else:
        print("Use: python migrate.py upgrade OR python migrate.py downgrade")