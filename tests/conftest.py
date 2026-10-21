import os
import tempfile

import pytest

# Must be set BEFORE the app is imported, because config.py reads them at import.
_db_file = os.path.join(tempfile.mkdtemp(), "test.db")
os.environ["DATABASE_URL"] = f"sqlite:///{_db_file}"
os.environ["SECRET_KEY"] = "test-only-secret-key-not-for-production-use-0123456789"

from fastapi.testclient import TestClient  # noqa: E402

from app.db.session import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)  # fresh database for every test
    with TestClient(app) as c:
        yield c
