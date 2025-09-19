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

-- =======================================================
-- SAMPLE DATA INSERTS
-- =======================================================

-- Insert into Users
INSERT INTO User (name, phone_number) VALUES
('Innocent Nkurunziza', '250791233547'),
('Ishimwe Diane', '250790777734'),
('Alex Robert', '250799200583'),
('Cash Deposit Agent', '250795963036'),
('System User', NULL);

-- Insert into Categories
INSERT INTO Transaction_Categories (name, description) VALUES
('Deposit', 'Deposited money into account'),
('Payment', 'Payment made to merchant'),
('Transfer', 'Money transferred between accounts'),
('Airtime', 'Airtime purchase'),
('Other', 'Miscellaneous transactions');

-- Insert into Transactions (sample from MoMo SMS)
INSERT INTO Transactions (sender_id, receiver_id, category_id, TxId, amount, fee, balance, time, sms_body) VALUES
(1, 2, 2, '76662021700', 2000.00, 0.00, 2000.00, '2024-05-10 16:30:51', 'You have received 2000 RWF...'),
(1, 2, 2, '73214484437', 1000.00, 0.00, 1000.00, '2024-05-10 16:31:39', 'Your payment of 1,000 RWF...'),
(1, 2, 2, '51732411227', 600.00, 0.00, 400.00, '2024-05-10 21:32:32', 'Your payment of 600 RWF...'),
(4, 1, 1, '17818959211', 40000.00, 0.00, 40400.00, '2024-05-11 18:43:49', 'A bank deposit of 40000 RWF...'),
(1, 3, 3, '82113964658', 3500.00, 0.00, 10880.00, '2024-05-12 13:34:25', 'Your payment of 3,500 RWF...');

-- Insert into Transaction_Users
INSERT INTO Transaction_Users (transaction_id, user_id, role) VALUES
(1, 1, 'sender'),
(1, 2, 'receiver'),
(2, 1, 'sender'),
(2, 2, 'receiver'),
(3, 1, 'sender'),
(3, 2, 'receiver'),
(4, 4, 'sender'),
(4, 1, 'receiver'),
(5, 1, 'sender'),
(5, 3, 'receiver');

-- Insert into System Logs
INSERT INTO System_Logs (transaction_id, log_type, message) VALUES
(1, 'info', 'Transaction processed successfully'),
(2, 'info', 'Transaction processed successfully'),
(3, 'warning', 'Balance low after transaction'),
(4, 'info', 'Deposit recorded'),
(5, 'error', 'Delayed confirmation message');

-- ==============================================================
-- TESTING SOME CRUD (Create, Read/Select, Update, Delete) 
-- ==============================================================

-- Show all records from transactions table
SELECT * FROM transactions;

-- Update: adjust in table "user" name
UPDATE User SET name = 'Steven Kayitare' WHERE id = 1;

-- Delete: remove a log from "system_Logs"
DELETE FROM System_Logs WHERE log_id = 5;

-- Create: insert a new transfer
INSERT INTO Transactions (sender_id, receiver_id, category_id, TxId, amount, fee, balance, time, sms_body)
VALUES (2, 1, 3, '99999995454', 500.00, 10.00, 950.00, NOW(), 'Transfer from Eliana Anick to Janick Andy');