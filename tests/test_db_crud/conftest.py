import pytest
from core import settings, engine
from db.models import Base

@pytest.fixture(scope='session', autouse=False)
def setup_db():
    assert settings.DEBUG == True
    #Base.metadata.drop_all(engine)
    #Base.metadata.create_all(engine)