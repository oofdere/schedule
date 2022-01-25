from flask import Flask, render_template, request
from deta import Deta
from datetime import datetime

app = Flask(__name__)

deta = Deta("b04ojdm7_DZ4b7NfKv8hcea7gAVddWrJq5w8RaPkf")
times = deta.Base("times")
shows = deta.Base("shows")
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def gen_show_titles():
    kv = {}
    for item in shows.fetch().items:
        kv[item["key"]] = item["title"]
    return kv
show_titles = gen_show_titles()

def gen_show_details():
    kv = {}
    for item in shows.fetch().items:
        kv[item["key"]] = item
    return kv
show_details = gen_show_details()
print(show_details)

@app.route("/")
def index():
    raw = times.fetch()
    schedule = raw.items
    return render_template("schedule.html", schedule=schedule, show_titles=show_titles)

@app.route("/stream")
def stream():
    raw = times.fetch()
    schedule = raw.items
    return render_template("stream.html", schedule=schedule, show_titles=show_titles, show_details=show_details, days=days)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        show = request.form['show']
        updates = request.form.items()
        for update in updates:
            update = update[0]
            if update == "show":
                continue
            update = update.split(":")
            entry = times.get(update[0])
            entry[update[1]] = show
            times.put(entry)
    raw = times.fetch()
    schedule = raw.items
    return render_template("edit.html", schedule=schedule, show_titles=show_titles, days=days)

def readable_hour(hour):
    hour = datetime.strptime(hour, "%H")
    return hour.strftime("%I%p")
app.jinja_env.globals.update(readable_hour=readable_hour)