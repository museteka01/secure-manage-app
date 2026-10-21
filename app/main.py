from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import Base, engine
from app.models import user  # noqa: F401  (registers the User table on Base)
from app.routers import auth, health, users


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Create tables on startup if they do not exist yet.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Secure Manage App", version="1.0.0", lifespan=lifespan)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Secure Manage App is running", "docs": "/docs"}
