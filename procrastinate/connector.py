import asyncio
from typing import Any, Callable, Dict, Iterable, List, Optional


class BaseConnector:
    json_dumps: Optional[Callable] = None
    json_loads: Optional[Callable] = None

    async def close_pool(self) -> None:
        pass

    async def execute_query(self, query: str, **arguments: Any) -> None:
        raise NotImplementedError

    async def execute_query_one(self, query: str, **arguments: Any) -> Dict[str, Any]:
        raise NotImplementedError

    async def execute_query_all(
        self, query: str, **arguments: Any
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def make_dynamic_query(self, query: str, **identifiers: str) -> str:
        raise NotImplementedError

    async def listen_notify(
        self, event: asyncio.Event, channels: Iterable[str]
    ) -> None:
        raise NotImplementedError
