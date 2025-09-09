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
    ├── test_parse_xml.py
    ├── test_clean_normalize.py
    └── test_categorize.py

