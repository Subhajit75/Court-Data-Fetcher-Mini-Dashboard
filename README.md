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
└── README.md # Project Documentation

~~~









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



