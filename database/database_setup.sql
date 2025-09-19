CREATE DATABASE IF NOT EXISTS momo_sms;
USE momo_sms;

CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique user identifier',
    name VARCHAR(50) NOT NULL COMMENT 'User full name',
    phone_number VARCHAR(15) NULL UNIQUE COMMENT 'User phone number',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation timestamp'
);