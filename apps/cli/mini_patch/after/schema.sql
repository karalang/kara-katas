CREATE TABLE products (
    sku TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    price_cents INTEGER NOT NULL
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE order_items (
    order_id INTEGER NOT NULL REFERENCES orders(id),
    sku TEXT NOT NULL REFERENCES products(sku),
    quantity INTEGER NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    status TEXT NOT NULL DEFAULT 'new',
    total_cents INTEGER NOT NULL
);

CREATE INDEX orders_by_customer ON orders(customer_id);
CREATE INDEX orders_by_status ON orders(status);
