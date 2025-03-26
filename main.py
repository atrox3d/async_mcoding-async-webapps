import json
import asyncio
import logging
from pathlib import Path
from typing import Any, Awaitable, Callable, MutableMapping

type Scope = MutableMapping[str, Any]
type Message = MutableMapping[str, Any]
type Receive = Callable[[], Awaitable[Message]]
type Send = Callable[[Message], Awaitable[None]]

logger = logging.getLogger("uvicorn")  # Get the uvicorn logger


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            logger.info(f"Encoding bytes: {obj!r}")
            return obj.decode('utf-8', errors='replace')  # Or 'latin-1', 'base64', etc.
        return json.JSONEncoder.default(self, obj)


total_connections = 0


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    global total_connections
    total_connections += 1
    current_connection = total_connections

    try:
        # Use the custom encoder here
        formatted_scope = json.dumps(scope, indent=4, cls=BytesEncoder)
    except TypeError as e:
        logger.error(f"Error during JSON serialization: {e}")
        formatted_scope = str(scope)  # Fallback to string representation

    logger.info(f'beginning connection {current_connection}, Scope: {formatted_scope}')
    
    logger.info(f'ending connection {current_connection}')


def main():
    import uvicorn

    # Use pathlib to get the module name
    module_name = Path(__file__).stem
    app_str = f"{module_name}:app"


    uvicorn.run(
        app_str,
        port=5000,
        log_level="info",
        use_colors=False,
        reload=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
