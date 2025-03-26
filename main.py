import json
import asyncio
from pathlib import Path

from helpers import BytesEncoder, logger
from custom_types import Scope, Message, Receive, Send
from handlers import handle_lifespan, handle_http


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
    if scope['type'] == 'lifespan':
        await handle_lifespan(scope, receive, send)
    elif scope['type'] == 'http':
        await handle_http(scope, receive, send)
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
