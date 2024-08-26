-- migrate:up
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    directions TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    source TEXT NOT NULL
);

-- migrate:down
DROP TABLE recipes;
