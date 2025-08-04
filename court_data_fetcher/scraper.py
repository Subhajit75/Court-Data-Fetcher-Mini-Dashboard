from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
from datetime import datetime
import time
from flask import Flask, render_template, request
from urllib.parse import urljoin
import os

BASE_URL = "https://delhihighcourt.nic.in/"

# MySQL Configuration - Updated for Render
DB_CONFIG = {
    "host": os.getenv('DB_HOST', 'localhost'),
    "user": os.getenv('DB_USER', 'root'),
    "password": os.getenv('DB_PASSWORD', ''),
    "database": os.getenv('DB_NAME', 'court_data')
}

app = Flask(__name__)

def save_query(case_type, case_number, filing_year, raw_response):
    """Save query details to MySQL database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                case_type VARCHAR(50),
                case_number VARCHAR(50),
                filing_year VARCHAR(4),
                timestamp DATETIME,
                raw_response LONGTEXT
            )
        """)
        cursor.execute("""
            INSERT INTO queries (case_type, case_number, filing_year, timestamp, raw_response)
            VALUES (%s, %s, %s, %s, %s)
        """, (case_type, case_number, filing_year, timestamp, raw_response))

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Query log saved to MySQL.")
    except Exception as e:
        print("❌ MySQL Insert Error:", e)

def fetch_case_details(case_type, case_number, filing_year):
    """Fetch case details including most recent PDF from Delhi High Court website"""
    options = Options()
    
    # Updated Chrome options for Render
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # For Render, we need to specify the Chrome binary location
    options.binary_location = os.getenv('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome')

    try:
        # Initialize ChromeDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=options
        )
        
        driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

        # Step 1: Solve CAPTCHA
        captcha_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'captcha') or contains(@id,'captcha')]"))
        )
        captcha_text = captcha_element.text.strip()

        # Step 2: Fill and submit form
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'case_type')]"))
        ).send_keys(case_type)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'case_number')]"))
        ).send_keys(case_number)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'case_year')]"))
        ).send_keys(filing_year)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'captcha')]"))
        ).send_keys(captcha_text)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]"))
        ).click()
        time.sleep(5)

        # Step 3: Parse main case details
        raw_response = driver.page_source
        soup = BeautifulSoup(raw_response, "html.parser")
        table = soup.find("table")
        
        if not table:
            raise Exception("No result table found")

        rows = table.find_all("tr")
        if len(rows) < 2:
            raise Exception("No data rows found")

        tds = rows[1].find_all("td")

        # Extract parties information
        parties_full = tds[2].get_text(" ", strip=True) if len(tds) >= 3 else "Not Found"
        parties = parties_full.upper().split("VS.")[0].strip() if "VS." in parties_full.upper() else parties_full

        # Extract dates
        listing_text = tds[3].get_text(" ", strip=True) if len(tds) >= 4 else ""
        filing_date, next_hearing = "Not Found", "Not Found"
        for part in listing_text.split():
            if part.count("/") == 2:
                if filing_date == "Not Found":
                    filing_date = part
                else:
                    next_hearing = part

        # Step 4: Enhanced PDF Extraction
        most_recent_pdf = None
        
        # Method 1: Check main table first
        for link in tds[1].find_all("a", href=True):
            if ".pdf" in link["href"].lower():
                most_recent_pdf = urljoin(BASE_URL, link["href"])
                print(f"Found PDF in main table: {most_recent_pdf}")
                break

        # Method 2: Check orders page if not found in main table
        if not most_recent_pdf:
            try:
                orders_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Orders"))
                )
                driver.execute_script("arguments[0].click();", orders_link)
                time.sleep(3)
                
                # Wait for orders table to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//table"))
                )
                
                # Get all PDF links from first column of orders table
                pdf_links = driver.find_elements(By.XPATH, "//table//tr[position()>1]/td[1]//a[contains(@href, '.pdf')]")
                
                if pdf_links:
                    most_recent_pdf = pdf_links[0].get_attribute("href")
                    if not most_recent_pdf.startswith("http"):
                        most_recent_pdf = urljoin(BASE_URL, most_recent_pdf)
                    print(f"Found PDF in orders table: {most_recent_pdf}")

            except Exception as e:
                print(f"Orders page error: {str(e)}")

        # Prepare result
        result_data = {
            "parties": parties,
            "filing_date": filing_date,
            "next_hearing": next_hearing,
            "pdf_link": most_recent_pdf
        }

        # Save to database
        save_query(case_type, case_number, filing_year, raw_response)

        return result_data, "✅ Case details fetched successfully!"

    except Exception as e:
        return None, f"❌ Error: {str(e)}"
    
    finally:
        if 'driver' in locals():
            driver.quit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        case_type = request.form["case_type"]
        case_number = request.form["case_number"]
        filing_year = request.form["filing_year"]

        result, message = fetch_case_details(case_type, case_number, filing_year)
        if result:
            return render_template("result.html", result=result)
        else:
            return render_template("result.html", error=message)
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
