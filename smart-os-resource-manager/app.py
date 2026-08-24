from flask import Flask,render_template,jsonify
import psutil
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/system")
def system_info():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage().percent
    processes = len(psutil.pids())

    return jsonify({
        "cpu": cpu,"memory": memory,
        "disk": disk,"processes": processes
    })

if __name__ == "__main__":
    app.run(debug=True)