from flask import Flask
from database import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    db = get_connection()

    if db.is_connected():
        return "MySql Connected"
    
    return "College Management System"

if __name__ == '__main__':
    app.run(debug=True)