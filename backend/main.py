from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS, CORS_ORIGIN_REGEX
from database import init_db
from routers import scan, history, auth

app = FastAPI(
    title="PhishGuard API",
    description="Фишинг сайттарды анықтау жүйесі / Система обнаружения фишинговых сайтов",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(scan.router, prefix="/api/v1", tags=["scan"])
app.include_router(history.router, prefix="/api/v1", tags=["history"])


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "PhishGuard API v1.0", "docs": "/docs"}
