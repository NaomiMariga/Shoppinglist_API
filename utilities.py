"""
Defines the frequently used functions
"""
import sqlalchemy


class Utilities:
    def database_connection(self):
        url = "postgresql://postgres:Theology@localhost:5432/shoppinglist"

        connection = sqlalchemy.create_engine(url)

        # binds connection to the metadata
        metadata = sqlalchemy.MetaData(bind=connection, reflect=True)

        "returns a connection and metadata"
        return connection, metadata

