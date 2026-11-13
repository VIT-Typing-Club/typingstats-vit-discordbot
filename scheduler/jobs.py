from config import DISCORD_CHANNEL_ID
from embeds.daily_leaderboard import create_daily_leaderboard_embed
from embeds.daily_quote import create_daily_quote_embed
from services.typingclub_api import get_daily_data
from storage.state import load_state, save_state


async def get_channel(bot):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)

    if channel is None:
        channel = await bot.fetch_channel(DISCORD_CHANNEL_ID)

    return channel


async def post_daily_quote(bot):
    print("[SCHEDULER] Fetching daily quote...")

    data = await get_daily_data()

    if data is None:
        print("[ERROR] Could not fetch daily quote.")
        return

    quote = data["quote"]
    quote_id = quote.get("quoteId")

    if not quote_id:
        print("[ERROR] Quote ID missing.")
        return

    state = load_state()

    if state.get("last_quote_id") == quote_id:
        print(f"[SKIP] Quote {quote_id} already published.")
        return

    channel = await get_channel(bot)

    embed = create_daily_quote_embed(quote)

    await channel.send(embed=embed)

    state["last_quote_id"] = quote_id
    save_state(state)

    print(f"[SUCCESS] Published daily quote: {quote_id}")


async def post_final_leaderboard(bot):
    print("[SCHEDULER] Fetching final leaderboard...")

    data = await get_daily_data()

    if data is None:
        print("[ERROR] Could not fetch leaderboard.")
        return

    quote_id = data["quote"].get("quoteId")
    leaderboard = data["leaderboard"]

    if not quote_id:
        print("[ERROR] Quote ID missing.")
        return

    if not leaderboard:
        print("[SKIP] No participants today. Leaderboard not published.")
        return

    state = load_state()

    if state.get("last_leaderboard_id") == quote_id:
        print(f"[SKIP] Leaderboard for {quote_id} already published.")
        return

    channel = await get_channel(bot)

    embed = create_daily_leaderboard_embed(leaderboard)

    await channel.send(embed=embed)

    state["last_leaderboard_id"] = quote_id
    save_state(state)

    print(f"[SUCCESS] Published leaderboard: {quote_id}")
