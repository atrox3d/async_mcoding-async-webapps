import json
import asyncio
import logging
from typing import Any, Awaitable, Callable, MutableMapping

type Scope = MutableMapping[str, Any]
type Message = MutableMapping[str, Any]
type Receive = Callable[[], Awaitable[Message]]
type Send = Callable[[Message], Awaitable[None]]

logger = logging.getLogger("uvicorn")  # Get the uvicorn access logger


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')  # Or 'latin-1', 'base64', etc.
        return json.JSONEncoder.default(self, obj)


total_connections = 0


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    global total_connections
    total_connections += 1
    current_connection = total_connections

    try:
        # Use the custom encoder here
        out_scope = json.dumps(scope, indent=4, cls=BytesEncoder)
    except TypeError as e:
        logger.error(f"Error during JSON serialization: {e}")
        out_scope = str(scope)  # Fallback to string representation

    logger.info(f'beginning connection {current_connection}, Scope: {out_scope}')
    logger.info(f'ending connection {current_connection}')


def main():
    import uvicorn
    uvicorn.run(
        app,
        port=5000,
        log_level="info",
        use_colors=False,
        # reload=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
