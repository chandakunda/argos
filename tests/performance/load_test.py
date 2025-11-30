"""
Simple async load test hitting /health endpoint.
"""

import asyncio
import httpx
import time

URL = "http://127.0.0.1:8000/health"

async def hit_endpoint(client):
    resp = await client.get(URL)
    return resp.status_code

async def run_load_test(concurrency=100):
    async with httpx.AsyncClient(timeout=2.0) as client:
        tasks = [hit_endpoint(client) for _ in range(concurrency)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

def test_load_performance():
    start = time.time()
    results = asyncio.run(run_load_test(50))
    duration = time.time() - start

    success = sum(1 for r in results if r == 200)
    assert success >= 40  # 80% success threshold
    assert duration < 3.0  # Should finish fast
