import time
from engine.config import get_int, get_float

def with_retry(fn, retriable_exceptions=(Exception,)):
    max_retries = get_int("BOUNDARY_MAX_RETRIES", 3)
    backoff = get_float("BOUNDARY_RETRY_BACKOFF_SECONDS", 1.5)
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            return fn()
        except retriable_exceptions as e:
            last_error = e
            if attempt == max_retries:
                break
            time.sleep(backoff * attempt)
    raise last_error
