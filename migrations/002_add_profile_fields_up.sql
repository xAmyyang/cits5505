-- ============================================================
-- Migration 002: Add Profile Fields
-- Description: Add bio, location, avatar_url to users table
--              and rename name column to username
-- ============================================================

-- forwards (up)
-- Step 1: create new users table with updated schema
CREATE TABLE IF NOT EXISTS users_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    bio TEXT,
    location TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Step 2: copy existing data across (name -> username)
INSERT INTO users_new (id, username, email, password_hash, created_at)
SELECT id, name, email, password_hash, created_at
FROM users;

-- Step 3: swap tables
DROP TABLE users;
ALTER TABLE users_new RENAME TO users;

-- backwards (down)
-- Step 1: recreate original users table
-- CREATE TABLE IF NOT EXISTS users_old (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     email TEXT NOT NULL UNIQUE,
--     password_hash TEXT NOT NULL,
--     created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
-- );
-- Step 2: copy data back (username -> name, drop bio/location/avatar_url)
-- INSERT INTO users_old (id, name, email, password_hash, created_at)
-- SELECT id, username, email, password_hash, created_at FROM users;
-- Step 3: swap tables
-- DROP TABLE users;
-- ALTER TABLE users_old RENAME TO users;
