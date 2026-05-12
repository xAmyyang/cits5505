-- 003_add_recipe_columns.sql
ALTER TABLE recipes ADD COLUMN emoji TEXT DEFAULT '🍽️';
ALTER TABLE recipes ADD COLUMN difficulty TEXT DEFAULT 'Easy 😌';
ALTER TABLE recipes ADD COLUMN likes INTEGER DEFAULT 0;
ALTER TABLE recipes ADD COLUMN status TEXT DEFAULT 'draft';

CREATE TABLE IF NOT EXISTS achievements (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    icon       TEXT NOT NULL,
    title      TEXT NOT NULL,
    desc       TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_achievements (
    user_id        INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,
    earned_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, achievement_id),
    FOREIGN KEY (user_id)        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE
);