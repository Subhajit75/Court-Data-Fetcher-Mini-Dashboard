# Delhi High Court Case Fetcher

## Project Overview
This project fetches case status from the **Delhi High Court** website.

### Features
- Fetch case details programmatically.
- Extracts:
  - Parties’ names
  - Filing & next-hearing dates
  - Most recent Order/Judgment PDF link
- CAPTCHA auto-solved (numeric) using headless Selenium.
- Logs raw responses to MySQL database.

### Setup Instructions
1. Clone this repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app locally:
   ```bash
   python app.py
   ```

### Deployment (Render)
1. Push this repo to GitHub.
2. Connect to Render.
3. Add a **Web Service**, set `Start Command` to:
   ```bash
   gunicorn app:app
   ```
4. Done!

### CAPTCHA Strategy
- The Delhi High Court site uses a **numeric CAPTCHA** which is auto-fetched.
- No external service is required.

### License
MIT License
