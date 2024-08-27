CREATE TABLE IF NOT EXISTS "schema_migrations" (version varchar(128) primary key);
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    directions TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    source TEXT NOT NULL,
    image TEXT
);
-- Dbmate schema migrations
INSERT INTO "schema_migrations" (version) VALUES
  ('20240816163836');
