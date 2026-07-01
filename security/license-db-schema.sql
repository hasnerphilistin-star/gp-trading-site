-- GP Trading — Esquema de Base de Datos de Auditoría de Licencias
-- SQLite

CREATE TABLE IF NOT EXISTS licencias (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    license_key     TEXT UNIQUE NOT NULL,
    producto        TEXT NOT NULL,
    product_id      TEXT NOT NULL,
    nt8_account_id  TEXT NOT NULL,
    customer_email  TEXT,
    customer_name   TEXT,
    order_id        TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    expires_at      TEXT,
    revocada        INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        TEXT UNIQUE NOT NULL,
    producto        TEXT NOT NULL,
    product_id      TEXT NOT NULL,
    monto           REAL,
    moneda          TEXT DEFAULT 'USDT',
    customer_email  TEXT,
    customer_name   TEXT,
    nt8_account_id  TEXT,
    payment_method  TEXT,
    payment_status  TEXT DEFAULT 'pending',
    created_at      TEXT DEFAULT (datetime('now')),
    completed_at    TEXT
);

CREATE INDEX IF NOT EXISTS idx_licencias_account
    ON licencias(nt8_account_id);

CREATE INDEX IF NOT EXISTS idx_licencias_product
    ON licencias(product_id);

CREATE INDEX IF NOT EXISTS idx_licencias_key
    ON licencias(license_key);

CREATE INDEX IF NOT EXISTS idx_orders_status
    ON orders(payment_status);
