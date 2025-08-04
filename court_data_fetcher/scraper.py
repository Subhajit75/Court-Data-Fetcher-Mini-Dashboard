import os, time, mysql.connector
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin

BASE_URL = "https://delhihighcourt.nic.in/"

# ✅ Auto DB Config (Local → MySQL, Render → PostgreSQL-like)
def get_db_config():
    if os.getenv('RENDER', '').lower() == 'true':
        return {
            "host": os.getenv('DB_HOST'),
            "user": os.getenv('DB_USER'),
            "password": os.getenv('DB_PASSWORD'),
            "database": os.getenv('DB_NAME'),
            "port": os.getenv('DB_PORT', 5432)
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
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                case_type VARCHAR(50),
                case_number VARCHAR(50),
                filing_year VARCHAR(10),
                timestamp DATETIME,
                raw_response LONGTEXT
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"DB init error: {e}", flush=True)
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if os.getenv('RENDER'):
        chrome_options.binary_location = os.getenv('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

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
        print(f"MySQL Insert Error: {e}", flush=True)
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def fetch_case_details(case_type, case_number, filing_year):
    driver = None
    try:
        driver = setup_driver()
        driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

        # Captcha
        captcha = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'captcha')]"))
        ).text.strip()
        print(f"DEBUG: Captcha = {captcha}", flush=True)

        # Form submit
        driver.find_element(By.ID, "case_type").send_keys(case_type)
        driver.find_element(By.ID, "case_number").send_keys(case_number)
        driver.find_element(By.ID, "case_year").send_keys(filing_year)
        driver.find_element(By.ID, "captcha").send_keys(captcha)
        driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
        time.sleep(5)

        # Parse result
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tds = soup.select('table tr:nth-child(2) td')

        if len(tds) < 4:
            return None, "❌ Case not found or invalid details"

        parties = tds[2].get_text(" ", strip=True).split("VS.")[0].strip()
        dates = [d for d in tds[3].get_text(" ", strip=True).split() if d.count('/') == 2]
        pdf_link = find_pdf_link(driver, tds[1])

        result = {
            "parties": parties,
            "filing_date": dates[0] if dates else "Not Found",
            "next_hearing": dates[1] if len(dates) > 1 else "Not Found",
            "pdf_link": pdf_link
        }

        save_query(case_type, case_number, filing_year, str(result))
        return result, "✅ Case details fetched successfully"

    except Exception as e:
        return None, f"❌ Error: {str(e)}"
    finally:
        if driver:
            driver.quit()

def find_pdf_link(driver, td_element):
    for link in td_element.find_all("a", href=True):
        if ".pdf" in link["href"].lower():
            return urljoin(BASE_URL, link["href"])
    return None
