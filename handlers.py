from custom_types import Receive, Scope, Send
from helpers import logger

async def handle_lifespan(scope: Scope, receive: Receive, send: Send) -> None:
    assert scope["type"] == "lifespan"
    while True:
        message = await receive()
        logger.info(f'got message: {message}')
        
        if message["type"] == "lifespan.startup":
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            await send({"type": "lifespan.shutdown.complete"})
            break
    

async def handle_http(scope: Scope, receive: Receive, send: Send) -> None:
    pass