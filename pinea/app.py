from fastapi import FastAPI

from pinea.routers import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="pinea",
    description="API para geração de OS.",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://pineaos-rafaelgonzagafrs-projects.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(os.router)