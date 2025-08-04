import mysql.connector
import config

def log_query(case_type, case_number, filing_year, raw_response):
    try:
        conn = mysql.connector.connect(**config.DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO queries (case_type, case_number, filing_year, raw_response)
            VALUES (%s, %s, %s, %s)
            """,
            (case_type, case_number, filing_year, raw_response)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(" Query logged to MySQL successfully.")
    except Exception as e:
        print(" Database insert error:", e)

