from flask import Flask, jsonify, render_template

from routes.scan_routes import scan_blueprint

app = Flask(__name__)
app.register_blueprint(scan_blueprint)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "SecureRepo",
    })


if __name__ == "__main__":
    app.run(debug=True)
