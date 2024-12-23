from fastapi import FastAPI
from src.routes import router
from src.database import Base, engine

# Get-Process python* | Select-Object Id,ProcessName
# Get-Process python* | Stop-Process -Force

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

