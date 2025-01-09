from fastapi import FastAPI
from src.routes.user_routes import router as router_users
from src.routes.todo_routes import router as router_todo
from src.database import Base, engine

# Get-Process python* | Select-Object Id,ProcessName
# Get-Process python* | Stop-Process -Force

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_users)

app.include_router(router_todo)

