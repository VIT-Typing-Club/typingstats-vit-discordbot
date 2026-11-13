import discord

MEDALS = ("🥇", "🥈", "🥉")

DISCORD_ID_KEY = "discordId"

def _name(player: dict) -> str:
    user_id = player.get(DISCORD_ID_KEY)

    if user_id:
        return f"<@{user_id}>"

    return player.get("displayName") or player.get("discordUsername") or "Unknown"


def _wpm(player: dict) -> float:
    return float(player.get("wpm", 0) or 0)


def _accuracy(player: dict) -> float:
    return float(player.get("accuracy", 0) or 0) * 100


def _quote_line(quote: dict) -> str:
    title = (quote.get("sourceTitle") or "Unknown source")[:80]
    quote_id = quote.get("quoteId")

    if not quote_id:
        return title

    url = f"https://typegg.io/solo/{quote_id}"
    return f"[{title}]({url})  ·  `{quote_id}`"


def create_daily_leaderboard_embed(data: dict) -> discord.Embed:
    quote = data.get("quote") or {}
    leaderboard = data.get("leaderboard") or []
    now = discord.utils.utcnow()

    embed = discord.Embed(
        title="Daily Competition Results",
        description=f"<t:{int(now.timestamp())}:D>\n{_quote_line(quote)}",
        color=discord.Color.from_rgb(240, 185, 11),
    )

    if not leaderboard:
        embed.description += "\n\nNo participants today. See you tomorrow."
        embed.set_footer(text="VIT Typing Club")
        return embed

    podium = "\n".join(
        f"{MEDALS[i]}  **{_name(p)}**  ·  {_wpm(p):.2f} WPM  ·  {_accuracy(p):.1f}%"
        for i, p in enumerate(leaderboard[:3])
    )
    embed.add_field(name="\u200b", value=podium, inline=False)

    if len(leaderboard) > 3:
        rest = "\n".join(
            f"`{rank}`  {_name(p)}  ·  {_wpm(p):.2f} WPM"
            for rank, p in enumerate(leaderboard[3:10], start=4)
        )
        embed.add_field(name="\u200b", value=rest, inline=False)

    count = len(leaderboard)
    embed.set_footer(
        text=f"VIT Typing Club  ·  {count} participant{'s' if count != 1 else ''}"
    )

    return embed