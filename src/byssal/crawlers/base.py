from abc import abstractmethod, ABC
from typing import Iterator

from byssal.threads.base import Thread


class Crawler(ABC):
    @abstractmethod
    def crawl(self) -> Iterator[Thread]:
        pass
