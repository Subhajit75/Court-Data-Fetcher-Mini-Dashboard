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
## ⚙️ Setup Steps

Follow these steps to run the this project locally:


### 1️⃣ Clone the Repository

```bash
   git clone https://github.com/your-username/Court-Data-Fetcher-Mini-Dashboard.git
cd Court-Data-Fetcher-Mini-Dashboard/court_data_fetcher
   ```

### 2️⃣ Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
   ```
 **Linux / Mac:**
 ```bash
python3 -m venv venv
source venv/bin/activate
  ```
**3️⃣ Install Project Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
## 📦 Key Dependencies

- Flask – Web framework for UI and routing
- Selenium – Browser automation for fetching data
- WebDriver Manager – Automatically manages ChromeDriver
- BeautifulSoup4 – HTML parsing to extract case details
- MySQL Connector – Save query logs in MySQL database

---
## 🔒 CAPTCHA Strategy

- The **Delhi High Court** case status page uses a **numeric text CAPTCHA**.
- Our script automatically handles this by:
  1. **Locating** the `<span>` element with the numeric CAPTCHA using:
     ```python
     captcha_element = WebDriverWait(driver, 20).until(
         EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'captcha') or contains(@id,'captcha')]"))
     )
     captcha_text = captcha_element.text.strip()
     ```
  2. **Extracting the numeric CAPTCHA text** directly from the DOM.
  3. **Filling it programmatically** into the form using:
     ```python
     driver.find_element(By.XPATH, "//input[contains(@id,'captcha')]").send_keys(captcha_text)
     ```
- **No manual input or external OCR service is needed**, since the CAPTCHA is already **plain text**.


**Note:**  
If the Delhi High Court changes the CAPTCHA to **image-based**, the following strategies can be used:  
- OCR with **Tesseract** to extract text from the image  
- Or manual token input through the web form  

---
##  Sample `.env` Variables

Create a `.env` file in the root folder with the following variables:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=court_data

FLASK_ENV=development
SECRET_KEY=secret123
```
---

## 🔄 Pagination for Multiple Orders

Some cases have multiple pages of **Orders** in the Delhi High Court portal.  
Our scraper automatically handles pagination to ensure the **latest order PDF** is always captured.

### Steps:

1. After navigating to the **Orders** page:
   - Detect the pagination elements (e.g., `Next` or numbered pages).
   - Loop through all pages using Selenium.

2. On each page:
   - Parse all **Case No / Order Link** rows.
   - Collect the **Date of Order** and corresponding **PDF link**.

3. After scanning all pages:
   - Compare dates and **select the most recent PDF**.

---
## 🧪 Simple Unit Tests

This project includes **basic unit tests** using **pytest** to validate core functionality:

1.  **Database Save Function** – Ensures `save_query()` inserts queries without errors.  
2. **Case Details Response Structure** – Confirms `fetch_case_details()` returns the expected dictionary structure.
3. ***Test File Name** *test_app.py*


## 📝 Sample Test (tests/test_app.py)
```python

import pytest
from scraper import save_query

def test_save_query(monkeypatch):
    """Check if save_query runs without raising an exception"""

    def mock_connect(**kwargs):
        class MockCursor:
            def execute(self, *args, **kwargs): pass
            def close(self): pass
        class MockConn:
            def cursor(self): return MockCursor()
            def commit(self): pass
            def close(self): pass
        return MockConn()

    import mysql.connector
    monkeypatch.setattr(mysql.connector, "connect", mock_connect)

    try:
        save_query("W.P.(C)", "1234", "2024", "<html>Mock Response</html>")
        assert True
    except Exception as e:
        pytest.fail(f"save_query raised an exception: {e}")


def test_fetch_case_details_structure(monkeypatch):
    """Check that fetch_case_details returns the correct dictionary structure"""

    from scraper import fetch_case_details

    def mock_fetch_case_details(case_type, case_number, filing_year):
        return {
            "parties": "DELHI PUBLIC LIBRARY",
            "filing_date": "27/11/2025",
            "next_hearing": "NA",
            "pdf_link": "https://delhihighcourt.nic.in/app/showlogo/1753885946_a72e225ba0bed7aa_598_12342024.pdf/2025"
        }, "✅ Mock success"

    monkeypatch.setattr("scraper.fetch_case_details", mock_fetch_case_details)

    result, message = fetch_case_details("W.P.(C)", "1234", "2024")

    assert isinstance(result, dict)
    assert "parties" in result
    assert "filing_date" in result
    assert "next_hearing" in result
    assert "pdf_link" in result
    assert ".pdf" in result["pdf_link"].lower()
```
## ▶️ Run the Tests
```brash
pytest -v
```
    
    


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
│ ├── tests/
│ │ └── test_app.py # Simple pytest unit test
│ │
│ ├── app.py # Flask main app
│ ├── scraper.py # Core Selenium scraping logic
│ ├── db.py # MySQL connection helper
│ ├── config.py # DB credentials & app config
│ ├── requirements.txt # Python dependencies
│ └── Dockerfile # Optional containerization
│
├── LICENSE # MIT License
└── README.md # Project Documentation

~~~






---
## 🎥 Demo

<p align="center">
  <img src="demo.gif" alt="Delhi High Court Case Status Demo" width="80%">
</p>
---

## 📫 Contact

<div align="center">

[![Email](https://img.shields.io/badge/Email-subhajitghosh7590%40gmail.com-red?style=flat&logo=gmail)](mailto:subhajitghosh7590@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Subhajit_Ghosh-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/subhajit-ghosh-75s90g/)
[![GitHub](https://img.shields.io/badge/GitHub-Subhajit75-black?style=flat&logo=github)](https://github.com/Subhajit75)

</div>

## 📜 License

MIT License © 2025 [Subhajit Ghosh](https://www.linkedin.com/in/subhajit-ghosh-75s90g/)

---

<div align="center">
  
Made by [Subhajit Ghosh](https://www.linkedin.com/in/subhajit-ghosh-75s90g/)  

</div>



