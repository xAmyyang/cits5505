import sqlite3

DB_PATH = "instance/survivechef.db"

conn = sqlite3.connect(DB_PATH)
db = conn.cursor()

new_columns = [
    "ALTER TABLE recipes ADD COLUMN emoji TEXT DEFAULT '🍽️'",
    "ALTER TABLE recipes ADD COLUMN difficulty TEXT DEFAULT 'Easy 😌'",
    "ALTER TABLE recipes ADD COLUMN likes INTEGER DEFAULT 0",
    "ALTER TABLE recipes ADD COLUMN status TEXT DEFAULT 'draft'",
]
for sql in new_columns:
    try:
        db.execute(sql)
        print(f"OK: {sql}")
    except sqlite3.OperationalError as e:
        print(f"SKIP: {e}")

db.execute("""
CREATE TABLE IF NOT EXISTS achievements (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    icon       TEXT NOT NULL,
    title      TEXT NOT NULL,
    desc       TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0
)
""")

db.execute("""
CREATE TABLE IF NOT EXISTS user_achievements (
    user_id        INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,
    earned_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, achievement_id),
    FOREIGN KEY (user_id)        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE
)
""")

count = db.execute("SELECT COUNT(*) FROM achievements").fetchone()[0]
if count == 0:
    db.executemany(
        "INSERT INTO achievements (icon, title, desc, sort_order) VALUES (?, ?, ?, ?)",
        [
            ("🍳", "First Cook",        "Posted your first recipe",   1),
            ("❤️", "Crowd Pleaser",     "Got 50+ likes",              2),
            ("📦", "5-Ingredient Hero", "Cooked with ≤5 ingredients", 3),
            ("🔥", "On Fire",           "Post 5 recipes",             4),
            ("🌟", "Rising Star",       "Get 100+ likes total",       5),
            ("👨‍🍳", "Master Chef",     "Post 20 recipes",            6),
        ]
    )
    print("OK: inserted default achievements")
else:
    print("SKIP: achievements already seeded")

conn.commit()
conn.close()
print("Done.")