-- ingredients
INSERT OR IGNORE INTO ingredients (name) VALUES
('egg'),
('rice'),
('spring onion'),
('bread'),
('milk'),
('tomato sauce'),
('pasta'),
('bacon');

-- recipes
INSERT OR IGNORE INTO recipes (title, description, instructions)
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
INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id)
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

-- additional ingredients
INSERT OR IGNORE INTO ingredients (name) VALUES
('kimchi'),
('cheese'),
('tuna'),
('potato'),
('mushroom'),
('chicken'),
('garlic'),
('ham'),
('onion'),
('carrot'),
('noodles'),
('butter'),
('mayonnaise'),
('sausage'),
('spinach'),
('tofu'),
('beans');

-- additional recipes
INSERT OR IGNORE INTO recipes (title, description, instructions)
VALUES
(
    'kimchi fried rice',
    'spicy korean fried rice',
    'stir fry kimchi and rice together'
),
(
    'cheese toast',
    'crispy cheesy toast',
    'toast bread and melt cheese on top'
),
(
    'tuna rice bowl',
    'easy tuna rice meal',
    'mix tuna with rice and mayonnaise'
),
(
    'potato omelette',
    'simple potato egg dish',
    'cook potato and egg together in pan'
),
(
    'mushroom pasta',
    'creamy mushroom pasta',
    'cook pasta and stir fry mushrooms'
),
(
    'chicken rice bowl',
    'easy chicken rice bowl',
    'cook chicken and serve over rice'
),
(
    'garlic butter pasta',
    'simple garlic pasta',
    'cook pasta with garlic and butter'
),
(
    'ham cheese sandwich',
    'quick sandwich recipe',
    'layer ham and cheese between bread'
),
(
    'scrambled egg toast',
    'soft egg breakfast toast',
    'cook scrambled egg and place on toast'
),
(
    'tomato egg stir fry',
    'classic tomato egg recipe',
    'cook tomato and egg together'
),
(
    'kimchi cheese rice',
    'cheesy kimchi rice bowl',
    'mix kimchi rice and cheese together'
),
(
    'mushroom egg bowl',
    'warm mushroom rice bowl',
    'cook mushrooms and egg over rice'
),
(
    'sausage fried rice',
    'savory fried rice recipe',
    'cook sausage with rice and onion'
),
(
    'spinach omelette',
    'healthy spinach egg dish',
    'cook spinach and egg together'
),
(
    'tofu rice bowl',
    'simple tofu rice bowl',
    'pan fry tofu and serve with rice'
),
(
    'chicken noodle soup',
    'warm noodle soup',
    'cook chicken and noodles in broth'
),
(
    'beans toast',
    'easy beans on toast',
    'heat beans and serve on toast'
);

-- additional recipe ingredients
INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id)
VALUES

-- kimchi fried rice
(4, 9),
(4, 2),
(4, 1),

-- cheese toast
(5, 4),
(5, 10),

-- tuna rice bowl
(6, 11),
(6, 2),
(6, 22),

-- potato omelette
(7, 12),
(7, 1),

-- mushroom pasta
(8, 13),
(8, 7),
(8, 17),

-- chicken rice bowl
(9, 14),
(9, 2),

-- garlic butter pasta
(10, 7),
(10, 17),
(10, 21),

-- ham cheese sandwich
(11, 18),
(11, 10),
(11, 4),

-- scrambled egg toast
(12, 1),
(12, 4),

-- tomato egg stir fry
(13, 1),
(13, 15),

-- kimchi cheese rice
(14, 9),
(14, 10),
(14, 2),

-- mushroom egg bowl
(15, 13),
(15, 1),
(15, 2),

-- sausage fried rice
(16, 23),
(16, 2),
(16, 19),

-- spinach omelette
(17, 24),
(17, 1),

-- tofu rice bowl
(18, 25),
(18, 2),

-- chicken noodle soup
(19, 14),
(19, 20),

-- beans toast
(20, 26),
(20, 4);