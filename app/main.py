from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Finance Data Chatbot API",
    description="API for querying finance data using natural language.",
    version="0.1.0"
)


app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Finance Chat Bot API is running."
    }


@app.get("/health")
def health_check():
    return{
        "status": "healthy",
        "service": "finance chatbot"
    }