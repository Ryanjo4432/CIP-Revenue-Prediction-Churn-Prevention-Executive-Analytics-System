-- all tables for the platform, postgres runs this on first startup

CREATE TABLE IF NOT EXISTS customers (
    customer_id     SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(150) UNIQUE NOT NULL,
    age             INT,
    location        VARCHAR(100),
    join_date       DATE DEFAULT CURRENT_DATE,
    is_active       BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id  SERIAL PRIMARY KEY,
    customer_id     INT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    amount          NUMERIC(12, 2) NOT NULL,
    category        VARCHAR(50),
    date            TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS predictions (
    prediction_id       SERIAL PRIMARY KEY,
    customer_id         INT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    churn_probability   FLOAT,
    revenue_prediction  NUMERIC(12, 2),
    clv                 NUMERIC(12, 2),
    predicted_at        TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS recommendations (
    recommendation_id   SERIAL PRIMARY KEY,
    customer_id         INT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    recommendation      TEXT NOT NULL,
    priority            VARCHAR(20) DEFAULT 'medium',
    created_at          TIMESTAMP DEFAULT NOW()
);

-- indexes so queries dont die when data gets big
CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_predictions_customer ON predictions(customer_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_customer ON recommendations(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);

-- some seed data so the dashboard isnt empty on first run
INSERT INTO customers (name, email, age, location, join_date) VALUES
    ('Alice Johnson',  'alice@example.com',  29, 'New York',    '2023-01-15'),
    ('Bob Smith',      'bob@example.com',    34, 'Los Angeles', '2023-03-22'),
    ('Carol White',    'carol@example.com',  41, 'Chicago',     '2022-11-05'),
    ('David Brown',    'david@example.com',  25, 'Houston',     '2024-01-10'),
    ('Eva Martinez',   'eva@example.com',    38, 'Phoenix',     '2022-08-30'),
    ('Frank Lee',      'frank@example.com',  52, 'Philadelphia','2021-06-18'),
    ('Grace Kim',      'grace@example.com',  27, 'San Antonio', '2023-07-04'),
    ('Henry Wilson',   'henry@example.com',  45, 'San Diego',   '2022-02-14'),
    ('Isla Davis',     'isla@example.com',   31, 'Dallas',      '2023-09-19'),
    ('Jack Taylor',    'jack@example.com',   36, 'San Jose',    '2021-12-01')
ON CONFLICT DO NOTHING;

INSERT INTO transactions (customer_id, amount, category, date) VALUES
    (1, 250.00,  'subscription', '2024-01-05'),
    (1, 89.99,   'addon',        '2024-02-10'),
    (2, 450.00,  'subscription', '2024-01-08'),
    (3, 120.00,  'subscription', '2024-01-12'),
    (3, 300.00,  'upgrade',      '2024-03-01'),
    (4, 75.00,   'subscription', '2024-02-20'),
    (5, 600.00,  'subscription', '2024-01-25'),
    (5, 200.00,  'addon',        '2024-03-15'),
    (6, 980.00,  'enterprise',   '2024-01-30'),
    (7, 150.00,  'subscription', '2024-02-05'),
    (8, 430.00,  'subscription', '2024-01-18'),
    (9, 55.00,   'subscription', '2024-03-22'),
    (10, 770.00, 'enterprise',   '2024-02-28');
