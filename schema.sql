CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    balance REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    recipient_id INTEGER,
    amount REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (recipient_id) REFERENCES users(id)
);

INSERT INTO users (username, password, balance) VALUES ('user1', 'password1', 1000.0);
INSERT INTO users (username, password, balance) VALUES ('user2', 'password2', 500.0);
INSERT INTO users (username, password, balance) VALUES ('user3', 'password3', 750.0);
INSERT INTO users (username, password, balance) VALUES ('user4', 'password4', 300.0);
INSERT INTO users (username, password, balance) VALUES ('user5', 'password5', 1200.0);
