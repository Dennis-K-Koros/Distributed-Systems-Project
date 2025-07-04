import asyncio
import aiohttp
from collections import Counter

url = "http://localhost:5000/home"
counter = Counter()
TOTAL_REQUESTS = 10000  #change this as needed

async def fetch(session):
    async with session.get(url) as response:
        data = await response.json()
        server_id = data["message"].split(":")[1].strip()
        counter[server_id] += 1

async def main():
    print(f"Sending {TOTAL_REQUESTS} requests to the load balancer...")
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session) for _ in range(TOTAL_REQUESTS)]
        await asyncio.gather(*tasks)

    print("\n✅ Request distribution summary:")
    total_count = sum(counter.values())
    for server, count in counter.items():
        print(f"{server}: {count} requests")

    print(f"\n📦 Total requests sent: {TOTAL_REQUESTS}")
    print(f"📥 Total responses received: {total_count}")
    if total_count < TOTAL_REQUESTS:
        print("⚠️ Some requests may have failed or timed out.")

if __name__ == "__main__":
    asyncio.run(main())
