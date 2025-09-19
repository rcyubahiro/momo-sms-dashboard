CREATE DATABASE IF NOT EXISTS momo_sms;
USE momo_sms;

CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique user identifier',
    name VARCHAR(50) NOT NULL COMMENT 'User full name',
    phone_number VARCHAR(15) NULL UNIQUE COMMENT 'User phone number',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation timestamp'
);

CREATE TABLE Transaction_Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique category identifier',
    name VARCHAR(200) NOT NULL COMMENT 'Category name',
    description VARCHAR(200) COMMENT 'Category description'
);

CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique transaction identifier',
    sender_id INT NOT NULL COMMENT 'FK to User - sender',
    receiver_id INT COMMENT 'FK to User - receiver',
    category_id INT NOT NULL COMMENT 'FK to Transaction_Categories',
    TxId VARCHAR(250) NOT NULL UNIQUE COMMENT 'Financial Transaction Id from SMS',
    amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0) COMMENT 'Transaction amount',
    fee DECIMAL(10,2) DEFAULT 0 CHECK (fee >= 0) COMMENT 'Transaction fee charged',
    balance DECIMAL(10,2) CHECK (balance >= 0) COMMENT 'Balance after transaction',
    time DATETIME NOT NULL COMMENT 'Transaction timestamp',
    sms_body TEXT COMMENT 'Original SMS body',
    CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES User(id),
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES User(id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id)
);

-- Indexes for faster lookups
CREATE INDEX idx_tx_time ON Transactions(time);
CREATE INDEX idx_tx_sender ON Transactions(sender_id);


CREATE TABLE Transaction_Users (
    transaction_id INT NOT NULL,
    user_id INT NOT NULL,
    role VARCHAR(20) NOT NULL COMMENT 'Role of user in transaction (sender/receiver/agent)',
    PRIMARY KEY (transaction_id, user_id),
    CONSTRAINT fk_tu_tx FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id),
    CONSTRAINT fk_tu_user FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE System_Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique log identifier',
    transaction_id INT NOT NULL COMMENT 'FK to Transactions',
    log_type VARCHAR(250) NOT NULL COMMENT 'Type of log entry (info/error/warning)',
    message TEXT COMMENT 'Log details',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Log creation timestamp',
    CONSTRAINT fk_log_tx FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id)
);
