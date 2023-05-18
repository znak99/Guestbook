from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import datetime
import mysql.connector
import info

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

mydb = mysql.connector.connect(
    host="localhost",
    user=info.user,
    password=info.password,
    database="guestbook"
)

@app.get("/")
def read_root(request: Request):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM contents")
    posts = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

@app.post("/")
def create_post(request: Request, content: str = Form(...)):
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()

    formatted_date = current_date.strftime("%Y/%m/%d")
    formatted_time = current_time.strftime("%H:%M:%S")

    text = content
    time = f"{formatted_date} {formatted_time}"

    cursor = mydb.cursor()
    cursor.execute(f"INSERT INTO contents VALUES (0, '{text}', '{time}')")
    mydb.commit()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM contents")
    posts = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
