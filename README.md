# 🏛️ Court-Data Fetcher & Mini-Dashboard

A Python + Flask-based web application to fetch **Court-Data Fetcher & Mini-Dashboard** (Delhi High Court case details).  
It programmatically retrieves:

- 👥 **Parties’ Names**  
- 📅 **Filing Date & Next Hearing Date**  
- 📄 **Order/Judgment PDF Link**  
- 💾 **Stores query history & raw HTML in MySQL database**  

---

## ⚖️ Court Chosen

**Delhi High Court – Case Status (Case Type Wise)**  
🔗 [https://delhihighcourt.nic.in/app/get-case-type-status](https://delhihighcourt.nic.in/app/get-case-type-status)

---


## 📂 File Structure
~~~
Court-Data-Fetcher-Mini-Dashboard/
│
├── court_data_fetcher/
│ ├── static/
│ │ └── style.css # Custom styling
│ │
│ ├── templates/
│ │ ├── index.html # Input form (Case Type, Number, Year)
│ │ └── result.html # Result display page
│ │
│ ├── app.py # Flask main app
│ ├── scraper.py # Core Selenium scraping logic
│ ├── db.py # MySQL connection helper
│ ├── config.py # DB credentials & app config
│ ├── requirements.txt # Python dependencies
│ └── Dockerfile # Optional containerization
│
├── LICENSE # MIT License

~~~
└── README.md # Project Documentation
