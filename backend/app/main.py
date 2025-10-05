from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes_summary import router as summary_router  

app = FastAPI(title="Grocery API (Stage 1)", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summary_router, prefix="/api/v1")            

@app.get("/health")
def health():
    return {"ok": True}
