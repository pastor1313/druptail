from django.core.management.base import BaseCommand
from ...models import Article, Catalog
from wagtail.core.models import Page
from drupal_sync.core import DrupalMigrationTool

import asyncio

class Command(BaseCommand):
    drupal_engine = DrupalMigrationTool(
        drupal_db_string="postgres://user:pass@postgres:5432/drupal",
        sql_file_name="drupal_articles.sql"
    )
    help = 'Sync pages with Drupal'

    def handle(self, *args, **options):
        home_page:Catalog = Page.objects.type(Catalog).first()
        articles = asyncio.run(self.drupal_engine.get_drupal())
        articles_exists_ids = [article.seo_title for article in home_page.get_children()]
        for key, article in articles.items():
            if f"{article['article_id']}-drupal-page" not in articles_exists_ids:
                page = Article(
                    seo_title = f"{article['article_id']}-drupal-page",
                    title=article['title'],
                    body=article['article_body']
                )

                new_page = home_page.add_child(instance=page)
                new_page.save_revision().publish()