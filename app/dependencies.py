import time

from fastapi import HTTPException, Response

count = 0
start_time = time.time()
reset_interval = 10
rq_limit = 50


def rate_limit(response: Response) -> None:
    global start_time
    global count

    if time.time() > start_time + reset_interval:
        start_time = time.time()
        count = 0

    if count >= rq_limit:
        raise HTTPException(
            status_code=428,
            detail={
                "error": "Rate limit exceeded",
                "timout": round(start_time + reset_interval - time.time(), 2) + 0.01,
            },
        )
    count += 1
    response.headers["X-app-rate-limit"] = f"{count}:{rq_limit}"
    return None
