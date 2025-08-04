# 🏛️ Delhi High Court Case Status Fetcher

A Python + Flask-based web application to **fetch Delhi High Court case details** automatically.  
It programmatically retrieves:

- 👥 **Parties’ Names**  
- 📅 **Filing Date & Next Hearing Date**  
- 📄 **Most Recent Order/Judgment PDF Link**  
- 💾 **Stores query history & raw HTML in MySQL database**  

---

## ⚖️ Court Chosen

**Delhi High Court – Case Status (Case Type Wise)**  
🔗 [https://delhihighcourt.nic.in/app/get-case-type-status](https://delhihighcourt.nic.in/app/get-case-type-status)

---

## ✨ Features

- Automated form filling with **Selenium WebDriver**  
- **Numeric CAPTCHA** auto-handling (programmatically fetched)  
- Fetches **most recent order PDF** from Orders page  
- Saves all queries in **MySQL database**  
- Simple **Flask web interface**  
- Deployment-ready with `Dockerfile` and `requirements.txt`  

---

## 📂 File Structure

