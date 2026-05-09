-- ingredients
INSERT INTO ingredients (name) VALUES
('egg'),
('rice'),
('spring onion'),
('bread'),
('milk'),
('tomato sauce'),
('pasta'),
('bacon');

-- recipes
INSERT INTO recipes (title, description, instructions)
VALUES
(
    'egg fried rice',
    'quick fried rice recipe',
    'cook rice and stir fry with egg'
),
(
    'french toast',
    'simple breakfast recipe',
    'dip bread in egg mixture and cook'
),
(
    'tomato pasta',
    'easy pasta recipe',
    'cook pasta and mix with sauce'
);

-- recipe ingredients
INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
VALUES
-- egg fried rice
(1, 1),
(1, 2),
(1, 3),

-- french toast
(2, 1),
(2, 4),
(2, 5),

-- tomato pasta
(3, 6),
(3, 7),
(3, 8);