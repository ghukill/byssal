import logging
from pathlib import Path
import sqlite3
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from byssal.crawlers.base import Crawler
    from byssal.threads.base import Thread

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self, data_directory: str | Path = "~/.byssal"):
        self.data_directory = self._prepare_data_directory(data_directory)

    def _prepare_data_directory(self, data_directory: str | Path):
        data_directory = Path(data_directory).expanduser()
        if not data_directory.exists():
            data_directory.mkdir()
        return data_directory

    @property
    def db_filepath(self):
        return self.data_directory / "byssal.sqlite"

    def get_connection(self):
        return sqlite3.connect(Path(self.db_filepath))

    def create_database(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            create_table_sql = """
            create table if not exists thread (
                thread_uuid str primary key,
                type text,
                sha256 text,
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
            insert into thread (thread_uuid, type, sha256, uri, date_created, active)
            values (?, ?, ?, ?, ?, ?);
            """
            cursor.execute(
                insert_sql,
                (
                    thread.thread_uuid,
                    thread.thread_type,
                    thread.sha256,
                    thread.uri,
                    thread.created,
                    thread.exists,
                ),
            )
            connection.commit()

    def run_crawlers(self, crawlers: list["Crawler"]):
        i = 0
        t0 = time.time()
        for crawler in crawlers:
            for thread in crawler.crawl():
                i += 1
                self.add_thread(thread)
                if i > 0 and i % 100 == 0:
                    logger.debug(f"Threads added: {i}, elapsed: {time.time() - t0}")
                    t0 = time.time()
        logger.debug(f"Threads added: {i}, elapsed: {time.time() - t0}")
