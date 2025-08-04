from flask import Flask, render_template, request
from scraper import fetch_case_details
from court_data_fetcher.scraper import fetch_case_details

import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["DEBUG"] = config.DEBUG

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        case_type = request.form["case_type"]
        case_number = request.form["case_number"]
        filing_year = request.form["filing_year"]

        result, message = fetch_case_details(case_type, case_number, filing_year)
        if result:
            return render_template("result.html", result=result, message=message)
        else:
            return render_template("result.html", error=message)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
