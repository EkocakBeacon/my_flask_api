from flask import Flask, request, jsonify
import logging
import pyodbc

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# SQL Server connection details
server = 'solvexus-beacon52-analytics.database.windows.net'
database = 'production'
username = 'beacon52-powerbi'
password = 'ocGTl8QAq4raUJOq642G4z4Z9fqH'
driver = '{ODBC Driver 17 for SQL Server}'  # Or '{ODBC Driver 18 for SQL Server}'

@app.route("/run", methods=["POST"])
def run_query():
    try:
        app.logger.debug(f"Received request data: {data}")
        data = request.get_json()
        query = data.get("query")

        if not query:
            return jsonify({"error": "Missing 'query' parameter"}), 400

        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}',
            timeout=10
        )

        cursor = conn.cursor()
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]

        app.logger.debug(f"Query successful, returning {len(result)} rows.")
        return jsonify({"result": result})

    except Exception as e:
        app.logger.error(f"Error running query: {e}")
        return jsonify({"error": str(e)}), 500

# Optional: for testing API availability
@app.route("/", methods=["GET"])
def home():
    return "API is live!", 200
