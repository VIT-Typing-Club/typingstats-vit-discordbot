import discord

MAX_QUOTE_LENGTH = 3800


def create_daily_quote_embed(quote: dict) -> discord.Embed:
    text = (quote.get("text") or "No quote available.").strip()
    source = quote.get("sourceTitle") or "Unknown source"
    difficulty = float(quote.get("difficulty", 0) or 0)
    quote_id = quote.get("quoteId")

    if len(text) > MAX_QUOTE_LENGTH:
        text = text[: MAX_QUOTE_LENGTH - 3] + "..."

    now = discord.utils.utcnow()
    words = len(text.split())

    embed = discord.Embed(
        title="Daily Challenge",
        description=f"<t:{int(now.timestamp())}:D>\n\n> {text}",
        color=discord.Color.from_rgb(240, 185, 11),
    )

    embed.add_field(name="Source", value=source[:1024], inline=True)
    embed.add_field(name="Difficulty", value=f"{difficulty:.2f}", inline=True)
    embed.add_field(name="Length", value=f"{words} words", inline=True)

    footer = "VIT Typing Club"

    if quote_id:
        embed.url = f"https://typegg.io/solo/{quote_id}"
        footer += f"  ·  Quote ID: {quote_id}"

    embed.set_footer(text=footer)

    return embed