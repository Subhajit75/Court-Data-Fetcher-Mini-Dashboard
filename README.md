# 🏛️ Court-Data Fetcher & Mini-Dashboard


[![Python CI](https://github.com/Subhajit75/Court-Data-Fetcher-Mini-Dashboard/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Subhajit75/Court-Data-Fetcher-Mini-Dashboard/actions/workflows/python-ci.yml)

**Court-Data Fetcher & Mini-Dashboard** is a Python + Flask-based web application that allows users to fetch **Delhi High Court** case details by providing the Case Type, Case Number, and Filing Year.  

The app:

- Provides a simple web UI for input
- Programmatically fetches case details from the **Delhi High Court public portal**
- Auto-handles numeric CAPTCHA
- Extracts **Parties’ Names**, **Filing & Next Hearing Dates**, and the **Most Recent Order/Judgment PDF**
- Stores every query and raw HTML response in **MySQL** for auditing
- Displays results in a clean dashboard with direct PDF download links
- Handles invalid inputs and site downtime gracefully


---

## ⚖️ Court Chosen

**Delhi High Court – Case Status (Case Type Wise)**  
🔗 [https://delhihighcourt.nic.in/app/get-case-type-status](https://delhihighcourt.nic.in/app/get-case-type-status)

---
## ⚙️ Setup Steps

Follow these steps to run the this project locally:


**1️⃣ Clone the Repository**

```bash
   git clone https://github.com/your-username/Court-Data-Fetcher-Mini-Dashboard.git
cd Court-Data-Fetcher-Mini-Dashboard/court_data_fetcher
   ```

**2️⃣ Create a Virtual Environment**

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

**4️⃣ Setup MySQL Database**

Create a Database and Table
```sql
CREATE DATABASE court_data;
USE court_data;

CREATE TABLE queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_type VARCHAR(50),
    case_number VARCHAR(50),
    filing_year VARCHAR(10),
    timestamp DATETIME,
    raw_response LONGTEXT
);
```

**5️⃣ Run the Flask App**
```bash
python app.py
```
- Then open: http://127.0.0.1:5000


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
3. **Test File Name** ***test_app.py***

**▶️ Run the Tests**
```brash
pytest -v
```
    

---
## 🔄 CI Workflow

- GitHub Actions is set up for automated testing.
- **File:** ***.github/workflows/python-ci.yml***

---
## 📂 File Structure
~~~
Court-Data-Fetcher-Mini-Dashboard/
├── .github/
│ └── workflows/
│  └── python-ci.yml       # CI workflow for GitHub Actions
│ 
├── court_data_fetcher/
│ ├── static/
│ │ ├──images/
│ │ │ ├──Court-Data Fetcher & Mini-Dashboard.gif 
│ │ │ ├──ui_home.png             #User Interface
│ │ │ └──ui_result.png            #Result Interface
│ │ └── style.css                # Custom styling
│ │
│ ├── templates/
│ │ ├── index.html                 # Input form (Case Type, Number, Year)
│ │ └── result.html                # Result display page
│ ├── tests/
│ │ └── test_app.py                # Simple pytest unit test
│ │
│ ├── app.py                       # Flask main app
│ ├── scraper.py                   # Core Selenium scraping logic
│ ├── db.py                         # MySQL connection helper
│ ├── config.py                   # DB credentials & app config
│ ├── requirements.txt             # Python dependencies
│ └── Dockerfile                  # Optional containerization
│
├── Demo_Video_Link_of_Task_1.txt # screen-capture showing end-to-end flow
├── LICENSE                      # MIT License
└── README.md                     # Project Documentation

~~~


---
## 🎨 User Interface

Here is the **Case Search Form (Home Page)**:

![User Interface](court_data_fetcher/static/images/ui_home.png)

---

## 📊 Result Interface

Here is the **Result Page showing case details and PDF download**:

![Result Interface](court_data_fetcher/static/images/ui_result.png)

---

## 🎥 Demo Video

Watch the step-by-step screen-capture showing end-to-end flow on YouTube:  
[Court Data Fetcher & Mini Dashboard by Subhajit Ghosh](https://youtu.be/v_utOk5ip4Y)

**Short Demo**
<p align="center">
  <img src="court_data_fetcher/static/images/Court-Data Fetcher & Mini-Dashboard.gif" alt="Court-Data Fetcher & Mini-Dashboard" width="80%">
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



