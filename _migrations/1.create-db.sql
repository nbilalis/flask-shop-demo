PRAGMA foreign_keys = off;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS address;

CREATE TABLE address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    street VARCHAR (50) NOT NULL,
    number VARCHAR (5)  NOT NULL,
    postcode VARCHAR (10) NOT NULL,
    area VARCHAR (50)  NOT NULL,
    country VARCHAR (50)  NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES customer (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS customer;

CREATE TABLE customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname VARCHAR (50) NOT NULL,
    lastname VARCHAR (50) NOT NULL,
    "e-mail" VARCHAR (100) NOT NULL,
    phone VARCHAR (15),
    date_of_birth DATE
);

DROP TABLE IF EXISTS customer_credentials;

CREATE TABLE customer_credentials (
    customer_id INTEGER PRIMARY KEY REFERENCES customer (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    username VARCHAR (20)  NOT NULL,
    password_hash VARCHAR (128) NOT NULL
);

DROP TABLE IF EXISTS "order";

CREATE TABLE "order" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    status VARCHAR (10) NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES customer (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS order_item;

CREATE TABLE order_item (
    order_id INTEGER NOT NULL REFERENCES "order" (id),
    product_id INTEGER NOT NULL REFERENCES product (id),
    quantity INTEGER NOT NULL DEFAULT (0),
    PRIMARY KEY (order_id, product_id)
);

DROP TABLE IF EXISTS product;

CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR (100) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL (6, 2) NOT NULL,
    discount_ratio REAL NOT NULL DEFAULT (0)                               ,
    stock INTEGER NOT NULL,
    is_hot INTEGER DEFAULT (0),
    category_id TEXT REFERENCES category (id)
);

DROP TABLE IF EXISTS category;

CREATE TABLE category (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    parent TEXT,
    other INTEGER DEFAULT (0)
);

COMMIT TRANSACTION;

PRAGMA foreign_keys = on;
