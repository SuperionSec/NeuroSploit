import uuid
import time


def uuid7() -> uuid.UUID:
    timestamp_ms = int(time.time() * 1000)
    timestamp_bytes = timestamp_ms.to_bytes(6, 'big')
    random_bytes = uuid.uuid4().bytes
    uuid_bytes = timestamp_bytes + random_bytes[:10]
    return uuid.UUID(bytes=uuid_bytes)
