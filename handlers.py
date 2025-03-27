from email import message
from custom_types import Receive, Scope, Send
from helpers import logger, BytesEncoder
import json



async def handle_lifespan(scope: Scope, receive: Receive, send: Send) -> None:
    assert scope["type"] == "lifespan"
    while True:
        message = await receive()
        logger.info(f'got message: {message}')
        
        if message["type"] == "lifespan.startup":
            logger.info(f'sending {{"type": "lifespan.startup.complete"}}')
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            await send({"type": "lifespan.shutdown.complete"})
            logger.info(f'sending {{"type": "lifespan.shutdown.complete"}}')
            break
    

async def handle_http(scope: Scope, receive: Receive, send: Send) -> None:
    assert scope["type"] == "http"
    while True:
        logger.info('waiting for messages...')
        message = await receive()
        formatted_message = json.dumps(message, indent=4, cls=BytesEncoder)
        logger.info(f'got message: {formatted_message}')
        
        if message["type"] == "http.disconnect":
            logger.error('dicsconnected from server')
            break
        
        if not message['more_body']:
            logger.warning('no more body, disconnecting')
            break
        
    response_start = {
        "type": "http.response.start",
        "status": 200,
        "headers": [
                        (
                            b'content-type', 
                            b'text/plain',
            )
        ]
    }
    formatted_response_start = json.dumps(response_start, indent=4, cls=BytesEncoder)
    logger.info(f'sending response start: {formatted_response_start}')
    await send(response_start)
    
    response_body = {
        "type": "http.response.body",
        "body": b"k",
        "more_body": False
    }
    formatted_response_body = json.dumps(response_body, indent=4, cls=BytesEncoder)
    logger.info(f'sending response body: {formatted_response_body}')
    await send(response_body)
