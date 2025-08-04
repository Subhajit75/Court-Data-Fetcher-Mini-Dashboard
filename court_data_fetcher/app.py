from flask import Flask, render_template, request
#from scraper import fetch_case_details
from court_data_fetcher.scraper import fetch_case_details

from court_data_fetcher import config
from court_data_fetcher.scraper import fetch_case_details, init_db
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        case_type = request.form.get("case_type")
        case_number = request.form.get("case_number")
        filing_year = request.form.get("filing_year")

        if not all([case_type, case_number, filing_year]):
            return render_template("result.html", error=" All fields are required")

        result, message = fetch_case_details(case_type, case_number, filing_year)
        return render_template("result.html", result=result, error=message)
    
    return render_template("index.html")


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
