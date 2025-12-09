
import asyncio
from services import get_market_trends
import logging

# Setup Logging to match services.py
logging.basicConfig(level=logging.INFO)

async def test():
    print("Fetching trends for Pearl Millet...")
    trends = await get_market_trends("Pearl Millet")
    print("\n--- Result ---")
    print(trends)
    print(f"Count: {len(trends)}")

if __name__ == "__main__":
    asyncio.run(test())
