-- migrate:up
CREATE TABLE recipe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    instructions TEXT NOT NULL
);

CREATE TABLE ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE recipe_has_ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity_amount INTEGER NOT NULL,
    quantity_unit TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);


-- migrate:down
DROP TABLE recipes;
DROP TABLE ingredients;
DROP TABLE recipe_has_ingredient;
