# app/api_server.py
from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
import io
from src.inference import infer

app = FastAPI()

@app.post("/vqa")
async def vqa_endpoint(image: UploadFile = File(...), question: str = Form(...)):
    contents = await image.read()
    pil = Image.open(io.BytesIO(contents)).convert("RGB")
    res = infer(pil, question)
    return res
