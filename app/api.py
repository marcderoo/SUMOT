from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de mon site Flask !"}

@app.get("/status")
def status():
    return {"status": "OK", "version": "1.0"}
