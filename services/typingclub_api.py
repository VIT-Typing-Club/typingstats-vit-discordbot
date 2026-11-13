import aiohttp

from config import API_URL


async def get_daily_data():
    timeout = aiohttp.ClientTimeout(total=15)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(API_URL) as response:

                response.raise_for_status()
                data = await response.json()

                if not isinstance(data, dict):
                    raise ValueError("Invalid API response")

                quote = data.get("quote")
                leaderboard = data.get("leaderboard", [])

                if not quote:
                    raise ValueError("Quote missing from API response")

                if not isinstance(leaderboard, list):
                    raise ValueError("Invalid leaderboard format")

                return {"quote": quote, "leaderboard": leaderboard}

    except aiohttp.ClientError as e:
        print(f"[API ERROR] {e}")
        return None

    except ValueError as e:
        print(f"[DATA ERROR] {e}")
        return None
