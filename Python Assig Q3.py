import configparser
import json
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

DB_NAME = "config_data.db"


def read_config_file(file_path):
    config = configparser.ConfigParser()

    try:
        config.read(file_path)

        if not config.sections():
            raise Exception("Configuration file is empty or unreadable.")

        data = {}

        for section in config.sections():
            data[section] = dict(config[section])

        return data

    except FileNotFoundError:
        print("Error: Configuration file not found.")
        return None
    except Exception as e:
        print(f"Error reading configuration file: {e}")
        return None


def save_to_database(json_data):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_json TEXT NOT NULL
            )
        """)

        cursor.execute("INSERT INTO config_store (config_json) VALUES (?)",
                       (json.dumps(json_data),))

        conn.commit()
        conn.close()
        print("Configuration saved to database.")

    except Exception as e:
        print(f"Database error: {e}")


@app.get("/config")
def get_config():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT config_json FROM config_store ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()

        if result:
            return jsonify(json.loads(result[0]))
        else:
            return jsonify({"error": "No configuration found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    config_data = read_config_file("config.ini")

    if config_data:
        print("Extracted Configuration:")
        print(json.dumps(config_data, indent=4))

        save_to_database(config_data)

    print("Starting API server...")
    app.run(host="0.0.0.0", port=5000)
