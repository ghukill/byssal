from pathlib import Path
import sqlite3
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from byssal.crawlers.base import Crawler
    from byssal.threads.base import Thread


class Repository:
    def __init__(self, db_filepath: str | Path):
        self.db_filepath = db_filepath

    def get_connection(self):
        return sqlite3.connect(str(self.db_filepath))

    def create_database(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            create_table_sql = """
            create table if not exists thread (
                thread_uuid str primary key,
                type text,
                md5 text,
                uri text,
                date_created datetime,
                active boolean
            );
            """
            cursor.execute(create_table_sql)
            connection.commit()

    def add_thread(self, thread: "Thread"):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            insert_sql = """
            insert into thread (thread_uuid, type, md5, uri, date_created, active)
            values (?, ?, ?, ?, ?, ?);
            """
            cursor.execute(
                insert_sql,
                (
                    thread.thread_uuid,
                    thread.thread_type,
                    thread.md5,
                    thread.uri,
                    thread.created,
                    thread.exists,
                ),
            )
            connection.commit()

    def run_crawlers(self, crawlers: list["Crawler"]):
        for crawler in crawlers:
            for thread in crawler.crawl():
                self.add_thread(thread)
