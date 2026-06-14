from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analyze import router

app = FastAPI(
    title="DermAssist AI"
)

# Allow CORS from everywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "DermAssist AI Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }