from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Members api route
@app.route("/members")
def members():
    return {"members": ["Member1", "Mmeber2", "Member3"]}


if __name__ == "__main__":
    app.run(debug=True)