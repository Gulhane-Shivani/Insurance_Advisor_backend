
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.database import engine, Base
from .routes import auth, contact, admin, insurance
import os
from dotenv import load_dotenv

load_dotenv()
# Create database tables
# In production, use migrations (like Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Insurance Advisor API",
    description="Backend for the Insurance Advisor Web Application",
    version="1.0.0"
)

# CORS Metadata
frontend_url = os.getenv("FRONTEND_URL", "https://insurance-advisor-tau.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        frontend_url,
        f"{frontend_url}/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(contact.router)
app.include_router(admin.router)
app.include_router(insurance.router)

@app.get("/")
def root():
    return {"message": "Welcome to Insurance Advisor API", "docs": "/docs"}
