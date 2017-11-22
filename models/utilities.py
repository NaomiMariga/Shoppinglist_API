"""
Defines the frequently used functions
"""
import os
import sqlalchemy


class Utilities:
    def database_connection(self):
        try:
            url = os.environ.get('DATABASE_URL', "postgresql://shoppinglist:Andela100@localhost:5432/shoppinglist")

            connection = sqlalchemy.create_engine(url)

            "returns a connection"
        except Exception as error:
            connection = None
            print(str(error))

        return connection



