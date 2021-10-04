import pytest
from models import BaseModel

# Truncate all tables
@pytest.fixture(autouse=True)
def reset_database():
    with BaseModel.session.begin():
        for table in BaseModel.metadata.tables:
            BaseModel.session.execute("TRUNCATE TABLE {} CASCADE".format(table))