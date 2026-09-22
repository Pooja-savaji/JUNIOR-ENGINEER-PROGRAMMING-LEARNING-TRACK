
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL,
    quantity INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

INSERT INTO categories VALUES
(1, 'Electronics'),
(2, 'Stationery');

INSERT INTO products VALUES
(1, 'Mouse', 500, 10, 1),
(2, 'Keyboard', 800, 5, 1),
(3, 'Notebook', 100, 20, 2);

SELECT * FROM products;

SELECT * FROM products 
WHERE price > 400;

UPDATE products
SET quantity = 15
WHERE id = 1;

DELETE FROM products
WHERE id = 3;

SELECT products.name, categories.name
FROM products
JOIN categories
ON products.category_id = categories.id;

SELECT category_id, COUNT(*) AS total_products
FROM products
GROUP BY category_id;
