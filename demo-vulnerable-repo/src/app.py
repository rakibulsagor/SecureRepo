from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# Config flaw: Wildcard CORS configuration
CORS(app, resources={r"/api/*": {"origins": "*"}})
# Another CORS wildcard match for the scanner
allow_origins = ["*"]

# Beginner mistake: hardcoded absolute developer system path
LOCAL_DIR = "C:\\Users\\D4rkman\\Documents\\securerepo\\backend\\data"

# Beginner mistake: hardcoded database username/password
db_user = "root"
db_pass = "123456"

# Git merge conflict marker committed by mistake
<<<<<<< HEAD
print("Initializing database production settings")
=======
print("Initializing database staging settings")
>>>>>>> e69de29bb2d1d6434b8b29ae775ad8c2e48c5391

@app.route("/")
def index():
    return jsonify({"status": "running", "environment": "development"})

if __name__ == "__main__":
    # Config flaw: running with debug=True in server start
    app.run(host="0.0.0.0", port=5000, debug=True)
