# Asyncio Python 3.7+ package comparision with Javascript async
# by default operates in single thread and CPU core
# and schedules tasks as coroutines to run in an event loop

import asyncio
#import requests incompatible because does not return awaitable tasks
# pyenv exec pip install aiohttp
import aiohttp
from aiohttp import ClientSession

# generator based coroutines removed since 3.10
# @asyncio.coroutine
# def worker(name, timeout_secs):
#   yield asyncio.sleep(timeout_secs)

async def worker(name: str, timeout_secs: int) -> str | Exception:
    if (timeout_secs < 0): raise Exception("bad job")
    print(name, " start job")
    # do something else in event loop while working for timeout secs
    await asyncio.sleep(timeout_secs)
    print(name, " end job")
    return "good job"

async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    print("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html


async def main() -> None:
    results = await asyncio.gather(
        worker("Fast", 1),
        worker("Avg", 2.5), 
        worker("Slow", 4),
        worker("Fail", -1),
        return_exceptions=True)
    print(results)
    try:
        results2 = await asyncio.gather(
        worker("Fail", -1),
        worker("Good", 1),
        return_exceptions=False)
        print(results2)
    except Exception as e:
        print("caught exception ", e)
    async with ClientSession() as session:
        result3 = await fetch_html("http://ip.jsontest.com/", session)
        print(result3)
    

# possible to get default event loop instance but not usually needed
#loop = asyncio.get_event_loop()
#try:
#    loop.run_until_complete(main())
#finally:
#    loop.close()

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main(), debug=True)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
