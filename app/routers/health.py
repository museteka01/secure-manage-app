import logging

from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.db.session import engine

router = APIRouter(prefix="/health", tags=["Health"])
logger = logging.getLogger(__name__)


@router.get("")
def health():
    """Liveness: the process is up. Used by Docker / load balancers."""
    return {"status": "ok"}


@router.get("/db")
def db_health(response: Response):
    """Readiness: the database answers. Returns 503 (not 200) when it is down,
    and never leaks the raw error text to the caller."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"database": "ok"}
    except Exception:
        logger.exception("Database health check failed")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"database": "unavailable"}
