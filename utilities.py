"""
Defines the frequently used functions
"""
import sqlalchemy


class Utilities:
    def database_connection(self):
        try:
            url = "postgresql://postgres:Theology@localhost:5432/shoppinglist"

            connection = sqlalchemy.create_engine(url)

            "returns a connection"
        except Exception as error:
            connection = None
            print(str(error))

        return connection

