import asyncio
from importlib.resources import read_text
from string import Template
from .sql import drupal
import asyncpg

def async_db(method):
    async def wrapper(*args, **kwargs):
        self: DrupalMigrationTool = args[0]
        self.connection = await asyncpg.connect(self.drupal_engine)
        async with self.connection.transaction():
            return await method(*args, **kwargs)
    return wrapper


class DrupalMigrationTool(object):

    def __init__(self, drupal_db_string, sql_file_name ):
        self.connection:asyncpg.Connection = None
        self.drupal_engine = drupal_db_string
        self.sql = sql_file_name


    @async_db
    async def get_drupal(self):
        query = Template(read_text(drupal, self.sql))
        articles_raw = [dict(r) for r in await self.connection.fetch(query.substitute())]
        articles = {}

        for article in articles_raw:
            articles_by_id = {
                "article_id": 0,
                "article_body": "",
                "title": "",
            }
            for key, value in article.items():
                articles_by_id[key] = value
            if articles_by_id["article_id"] in articles:
                articles[articles_by_id["article_id"]].update(articles_by_id)
            else:
                articles[articles_by_id["article_id"]] = articles_by_id
        return articles