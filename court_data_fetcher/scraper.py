import os
import time
from datetime import datetime
from urllib.parse import urljoin
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import mysql.connector

BASE_URL = "https://delhihighcourt.nic.in/"
app = Flask(__name__)

# --------------------- Database Configuration ---------------------
def get_db_config():
    if os.getenv('RENDER', '').lower() == 'true':
        return {
            "host": os.getenv('DB_HOST'),
            "user": os.getenv('DB_USER'),
            "password": os.getenv('DB_PASSWORD'),
            "database": os.getenv('DB_NAME'),
            "port": int(os.getenv('DB_PORT', 3306))
        }
    else:
        return {
            "host": "localhost",
            "user": "root",
            "password": "subhajit",
            "database": "court_data",
            "port": 3306
        }

DB_CONFIG = get_db_config()

def init_db():
    """Create queries table if not exists"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                case_type VARCHAR(50),
                case_number VARCHAR(50),
                filing_year VARCHAR(4),
                timestamp TIMESTAMP,
                raw_response LONGTEXT
            )
        """)
        conn.commit()
    except Exception as e:
        print(f" DB init error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# --------------------- ChromeDriver Setup ---------------------
def setup_driver():
    # Auto-install compatible ChromeDriver
    chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Render uses pre-installed Chromium
    chrome_options.binary_location = "/usr/bin/chromium"

    return webdriver.Chrome(options=chrome_options)

# --------------------- Case Fetching Logic ---------------------
def fetch_case_details(case_type, case_number, filing_year):
    driver = None
    try:
        driver = setup_driver()
        driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

        # Solve Captcha
        captcha = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'captcha')]"))
        ).text.strip()

        # Fill form
        driver.find_element(By.XPATH, "//select[@id='case_type']").send_keys(case_type)
        driver.find_element(By.XPATH, "//input[@id='case_number']").send_keys(case_number)
        driver.find_element(By.XPATH, "//select[@id='case_year']").send_keys(filing_year)
        driver.find_element(By.XPATH, "//input[@id='captcha']").send_keys(captcha)
        driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
        time.sleep(5)

        # Parse table
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tds = soup.select('table tr:nth-child(2) td')

        if len(tds) < 4:
            return None, " Case not found or invalid details"

        # Parties & Dates
        parties = tds[2].get_text(" ", strip=True).split("VS.")[0].strip()
        dates = [d for d in tds[3].get_text(" ", strip=True).split() if d.count('/') == 2]

        # Most recent PDF
        pdf_link = find_pdf_link(driver, tds[1])

        result = {
            "parties": parties,
            "filing_date": dates[0] if dates else "Not Found",
            "next_hearing": dates[1] if len(dates) > 1 else "Not Found",
            "pdf_link": pdf_link
        }

        save_query(case_type, case_number, filing_year, str(result))
        return result, None

    except Exception as e:
        return None, f" Error: {str(e)}"
    finally:
        if driver:
            driver.quit()

# --------------------- PDF Extraction ---------------------
def find_pdf_link(driver, td_element):
    # Method 1: Main table
    for link in td_element.find_all("a", href=True):
        if ".pdf" in link["href"].lower():
            return urljoin(BASE_URL, link["href"])

    # Method 2: Orders page
    try:
        driver.find_element(By.LINK_TEXT, "Orders").click()
        time.sleep(3)
        pdf_links = driver.find_elements(By.XPATH, "//table//a[contains(@href, '.pdf')]")
        if pdf_links:
            pdf_url = pdf_links[0].get_attribute('href')
            return pdf_url if pdf_url.startswith('http') else urljoin(BASE_URL, pdf_url)
    except:
        pass

    return None

# --------------------- Save Query ---------------------
def save_query(case_type, case_number, filing_year, raw_response):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO queries (case_type, case_number, filing_year, timestamp, raw_response)
            VALUES (%s, %s, %s, %s, %s)
        """, (case_type, case_number, filing_year, datetime.now(), raw_response))
        conn.commit()
    except Exception as e:
        print(f" Save query error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# --------------------- Flask Routes ---------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        case_type = request.form.get("case_type")
        case_number = request.form.get("case_number")
        filing_year = request.form.get("filing_year")

        if not all([case_type, case_number, filing_year]):
            return render_template("result.html", error=" All fields are required")

        result, error = fetch_case_details(case_type, case_number, filing_year)
        return render_template("result.html", result=result, error=error)
    
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
