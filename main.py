from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts = []

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
def create_post(request: Request, content: str = Form(...)):
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()

    formatted_date = current_date.strftime("%Y/%m/%d")
    formatted_time = current_time.strftime("%H:%M:%S")
    post = {"content": content, "datetime": f"{formatted_date} {formatted_time}"}
    posts.append(post)
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
