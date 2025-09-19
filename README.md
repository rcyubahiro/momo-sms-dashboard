# MoMo SMS Data Processing and Dashboard

##  Team
- Team Name: *TEAM 4*  
- Members:  
  - Diane INGABIRE – GitHub: [@ingdia](https://github.com/ingdia)  
  - Innocent Nkurunziza – GitHub: [@innocent-gift](https://github.com/innocent-gift)  
  - Robert Cyubahiro – GitHub: [@rcyubahiro](https://github.com/rcyubahiro)  
  - Steven Kayitare – GitHub: [@stevenalu](https://github.com/stevenalu)
---

## Project Description  
This project is an **enterprise-level fullstack application** designed to process and analyze **MoMo SMS transaction data**. The workflow includes:

1. **Data Ingestion** – Extract raw XML SMS data.  
2. **ETL Pipeline** – Parse, clean, normalize, and categorize transactions.  
3. **Database Storage** – Store processed data into a relational database (SQLite for now).  
4. **Frontend Dashboard** – Provide an interface to visualize analytics such as transaction volume, categories, and trends.  

This project demonstrates backend data processing, database management, and frontend visualization skills.

## Project System Architecture  
[View Architecture Diagram](https://drive.google.com/file/d/1Lt3Uqu4GE6lg4vb1-AVCBusow0qvaAYg/view)  
<img width="355" height="531" alt="image" src="https://github.com/user-attachments/assets/dc057377-3c4b-4369-8035-27b6d93d2711" />



---

## Task Allocation  
[View Scrum Board on Trello](https://trello.com/invite/b/68bef5f1b5401a6a7143db5a/ATTI2a337ad2404e8b57a6df4bd9f3050eb9E17A53C5/agile-board-template-trello) 
<img width="1039" height="652" alt="image" src="https://github.com/user-attachments/assets/0a821eb9-b5be-423c-8f3b-d41e3955b236" />


##  Project Structure 

```bash
.
├── README.md                         # Setup, run, overview
├── .env.example                      # DATABASE_URL or path to SQLite
├── requirements.txt                  # Dependencies (lxml, dateutil, etc.)
├── index.html                        # Dashboard entry
├── website/
│   ├── styles.css                    # Dashboard styling
│   ├── chart_handler.js              # Render charts/tables
│   └── assets/                       # Icons/images
├── data/
│   ├── raw/                          # Raw XML inputs
│   ├── processed/                    # JSON outputs for frontend
│   ├── db.sqlite3                    # Database file
│   └── logs/                         # ETL logs & dead letters
├── etl/                              # ETL scripts
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
├── api/                              # Optional FastAPI backend
│   ├── app.py
│   ├── db.py
│   └── schemas.py
├── scripts/                          # Helper scripts
│   ├── run_etl.sh
│   └── serve_frontend.sh
└── tests/                            # Unit tests
│    ├── test_parse_xml.py
│    ├── test_clean_normalize.py
│    └── test_categorize.py
└── database
│    └── databse_setup.sql
└── Examples
      └── json_schemas.json


# MoMo SMS Data Processing System

## 📌 Overview
This project implements the **database foundation** for processing MoMo SMS transaction data.  
It is designed to support data ingestion, storage, querying, and analysis of different types of mobile money transactions, while ensuring data integrity, security, and scalability.

---

## 📂 Repository Structure
docs/erd_diagram.png # ERD diagram (exported from draw.io / Lucidchart)
database/database_setup.sql # MySQL schema with sample data
examples/json_schemas.json # JSON serialization examples
README.md # Database documentation (this file)

---

## 🗂️ Entity Relationship Diagram (ERD)
The database schema includes five main entities:

- **Users** – stores customer, merchant, and agent information  
- **Transactions** – central fact table for all MoMo operations  
- **Transaction Categories** – taxonomy of transaction types (e.g., P2P, Bill Payment)  
- **Transaction ↔ Categories Mapping** – junction table resolving many-to-many relation  
- **System Logs** – operational logging for data processing pipeline  

![ERD Diagram](docs/erd_diagram.png)

---

## 🛠️ Database Design Rationale
The schema models MoMo mobile-money SMS transaction data with clear separation of concerns for flexibility and analytics.  

- The **Users table** stores sender/receiver profiles so individuals can appear in multiple transactions without duplication.  
- **Transactions** is the central fact table, capturing amounts, references, timestamps, and links to users.  
- **Transaction Categories** provides a taxonomy for transaction types, while a junction table (`transaction_category_map`) resolves the many-to-many relationship between transactions and categories.  
- **System Logs** track data processing events and provide traceability.  

Referential integrity is enforced through foreign keys, with indexes for frequent queries.  
Constraints such as non-negative amounts and restricted statuses improve data quality.  
The design balances normalization for consistency with performance needs, supporting both analytics and operational workflows.  

---

## 📑 Data Dictionary (Summary)

| Table                     | Column              | Type            | Description                                               |
|----------------------------|---------------------|-----------------|-----------------------------------------------------------|
| **users**                 | user_id             | INT (PK)        | Unique user identifier                                    |
|                            | full_name           | VARCHAR(150)    | Full name of the user                                     |
|                            | phone               | VARCHAR(20)     | Unique phone number in E.164 format                       |
|                            | email               | VARCHAR(255)    | Optional email address                                    |
|                            | is_kyc_done         | TINYINT(1)      | 1 if KYC completed                                        |
|                            | user_role           | ENUM            | Role: customer, merchant, agent, system                   |
| **transactions**          | transaction_id      | BIGINT (PK)     | Internal transaction identifier                           |
|                            | momo_reference      | VARCHAR(100)    | Provider transaction reference                            |
|                            | amount              | DECIMAL(13,2)   | Transaction amount (>= 0)                                 |
|                            | currency            | CHAR(3)         | ISO currency code (e.g., RWF)                             |
|                            | occurred_at         | DATETIME        | Time the transaction occurred                             |
|                            | sender_id           | INT (FK)        | FK → users (sender)                                       |
|                            | receiver_id         | INT (FK)        | FK → users (receiver)                                     |
|                            | direction           | ENUM            | Transaction direction: IN/OUT                             |
|                            | status              | ENUM            | Transaction status: PENDING, COMPLETED, FAILED, REVERSED  |
|                            | raw_payload         | JSON            | Original SMS/XML payload for audit                        |
| **transaction_categories**| category_id         | INT (PK)        | Unique category identifier                                |
|                            | code                | VARCHAR(50)     | Short category code (e.g., P2P, BILL)                     |
|                            | name                | VARCHAR(120)    | Human-readable category name                              |
| **transaction_category_map** | map_id            | INT (PK)        | Junction table PK                                         |
|                            | transaction_id      | BIGINT (FK)     | FK → transactions                                         |
|                            | category_id         | INT (FK)        | FK → transaction_categories                               |
| **system_logs**           | log_id              | BIGINT (PK)     | Unique log identifier                                     |
|                            | processing_stage    | VARCHAR(80)     | Stage of data pipeline (ingest, parse, reconcile, etc.)   |
|                            | severity            | ENUM            | Log severity: DEBUG, INFO, WARN, ERROR                    |
|                            | message             | TEXT            | Log message details                                       |
|                            | transaction_id      | BIGINT (FK)     | Optional FK to related transaction                        |
|                            | meta                | JSON            | Structured metadata                                       |

---

## ⚙️ How to Run Locally
1. Clone this repo:
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
Start MySQL and create the database:

bash
Copy code
mysql -u root -p < database/database_setup.sql
Verify tables:

sql
Copy code
USE momoprocessing;
SHOW TABLES;
📦 JSON Examples
All entity examples are in
examples/json_schemas.json.

They include:

User JSON

Transaction Category JSON

Transaction JSON

Full Transaction JSON (with sender, receiver, categories)

✅ Sample Queries
Get completed transactions

sql
Copy code
SELECT transaction_id, momo_reference, amount, status
FROM transactions
WHERE status='COMPLETED';
Join transactions with users

sql
Copy code
SELECT t.transaction_id, u1.full_name AS sender, u2.full_name AS receiver, t.amount
FROM transactions t
LEFT JOIN users u1 ON t.sender_id = u1.user_id
LEFT JOIN users u2 ON t.receiver_id = u2.user_id;
Get categories per transaction

sql
Copy code
SELECT t.transaction_id, GROUP_CONCAT(c.name) AS categories
FROM transactions t
JOIN transaction_category_map m ON t.transaction_id = m.transaction_id
JOIN transaction_categories c ON m.category_id = c.category_id
GROUP BY t.transaction_id;
👥 Team Collaboration
All commits are tracked via GitHub

ERD exported to /docs

SQL scripts stored in /database

JSON examples stored in /examples

Scrum board updated weekly for sprint tracking

🤖 AI Usage Policy
✅ AI used for grammar, formatting, and syntax verification

❌ AI not used for logic, schema design, or reflection writing

AI interactions logged in AI_USAGE_LOG.md

📌 Deliverables
ERD Diagram in 

SQL Setup Script: database/database_setup.sql

JSON Examples: docs/erd_diagram.pdf

Database Design Document (integrated here in README)
