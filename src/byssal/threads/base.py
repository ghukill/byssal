from abc import abstractmethod, ABC
import datetime

THREAD_REGISTRY = {}


class Thread(ABC):
    """Represents a known resource thread."""

    thread_type: str = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.thread_type is None:
            raise ValueError(f"{cls.__name__} must define a thread_type class attribute")
        THREAD_REGISTRY[cls.thread_type] = cls

    def __init__(
        self,
        thread_uuid: str,
        md5: str,
        uri: str,
        created: datetime.datetime,
        exists: bool | None = None,
    ):
        self.thread_uuid = thread_uuid
        self.md5 = md5
        self.uri = uri
        self.created = created
        self._exists = exists

    @abstractmethod
    def calculate_md5(self):
        pass

    @abstractmethod
    def check_exists(self) -> bool:
        pass

    @property
    def exists(self):
        if not self._exists:
            self._exists = self.check_exists()
        return self._exists

    @abstractmethod
    def read(self) -> bytes:
        pass
