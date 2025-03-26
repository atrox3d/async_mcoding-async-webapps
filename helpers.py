import logging
import json

logger = logging.getLogger("uvicorn")  # Get the uvicorn logger

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            logger.info(f"Encoding bytes: {obj!r}")
            return obj.decode('utf-8', errors='replace')  # Or 'latin-1', 'base64', etc.
        return json.JSONEncoder.default(self, obj)