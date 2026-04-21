from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.database import engine, Base
from .routes import auth, contact

# Create database tables
# In production, use migrations (like Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Insurance Advisor API",
    description="Backend for the Insurance Advisor Web Application",
    version="1.0.0"
)

# CORS Metadata
# Adjust 'allow_origins' for production (e.g., ['https://yourfrontend.com'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(contact.router)

@app.get("/")
def root():
    return {"message": "Welcome to Insurance Advisor API", "docs": "/docs"}
