from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from deta import Deta
from app import views

app = FastAPI()

deta = Deta("b04ojdm7_DZ4b7NfKv8hcea7gAVddWrJq5w8RaPkf")
shows = deta.Base("shows")
times = deta.Base("times")

@app.get("/show/{slug}")
def get_show(slug: str):
    show = shows.get(slug)
    return show

@app.get("/schedule/{day}/{hour}")
def show_by_time(day: str, hour: int):
    days = times.get(f"{hour:02}")
    id = days[day]
    show = shows.get(id)
    return show

@app.get("/schedule")
def get_full_schedule():
    raw = times.fetch()
    return raw.items

@app.get("/views/stream")
def stream_view(request: Request):
    pass
