from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import cohere

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

cohere_api_key = "h88syAHDjKT8ey3wuSak5J5IfYusQoTG7oLzyR5u"
co = cohere.Client(cohere_api_key)

class TextToSummarize(BaseModel):
    text: str

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/summarize")
async def summarize(text: TextToSummarize):
    try:
        response = co.summarize(
            text=text.text,
            length="medium",  # Adjust based on your needs
            format="paragraph",  # Adjust based on your needs
            model="command",  # Adjust based on your needs
            extractiveness="low",  # Adjust based on your needs
            temperature=0.3  # Adjust based on your needs
        )
        summary = response['summary']  # Access the summary from the response dictionary
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
