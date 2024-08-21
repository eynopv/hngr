CREATE TABLE IF NOT EXISTS "schema_migrations" (version varchar(128) primary key);
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    instructions TEXT NOT NULL
);
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE recipe_ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    unit TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);
-- Dbmate schema migrations
INSERT INTO "schema_migrations" (version) VALUES
  ('20240816163836');
