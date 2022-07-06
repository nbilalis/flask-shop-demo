PRAGMA foreign_keys = off;

BEGIN TRANSACTION;

INSERT INTO customer (id, firstname, lastname, "e-mail", phone)
VALUES (1, 'Elon', 'Musk', 'elon@tesla.com', '12345567890');

INSERT INTO customer_credentials (customer_id, username, password_hash)
VALUES (1, 'elon', 'Ax-e762');

COMMIT TRANSACTION;

PRAGMA foreign_keys = on;
