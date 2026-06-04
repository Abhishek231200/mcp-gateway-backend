import time
from collections import defaultdict, deque
from fastapi import HTTPException

RATE_LIMIT = 100       # requests
WINDOW_SEC = 60        # per minute

_request_log: dict[str, deque] = defaultdict(deque)

def check_rate_limit(api_key: str) -> None:
    """Raise HTTP 429 if api_key exceeds RATE_LIMIT requests per WINDOW_SEC."""
    now = time.monotonic()
    window = _request_log[api_key]

    # Drop timestamps outside the rolling window
    while window and window[0] < now - WINDOW_SEC:
        window.popleft()

    if len(window) >= RATE_LIMIT:
        retry_after = int(WINDOW_SEC - (now - window[0])) + 1
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {RATE_LIMIT} requests/{WINDOW_SEC}s per API key.",
            headers={"Retry-After": str(retry_after)},
        )

    window.append(now)
