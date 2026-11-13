import logging

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands

from config import DISCORD_TOKEN, TIMEZONE
from embeds.daily_leaderboard import create_daily_leaderboard_embed
from embeds.daily_quote import create_daily_quote_embed
from scheduler.jobs import post_daily_quote, post_final_leaderboard
from services.typingclub_api import get_daily_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
log = logging.getLogger("typingclub")

intents = discord.Intents.default()
intents.message_content = True


class TypingClubBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="-", intents=intents)
        self.scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    async def setup_hook(self):
        """Runs once before the bot connects, so jobs are never registered twice."""
        self._register_jobs()
        self.scheduler.start()

        for job in self.scheduler.get_jobs():
            log.info("Scheduled %s -> next run %s", job.id, job.next_run_time)

    def _register_jobs(self):
        jobs = (
            # (function, job id, hour, minute, misfire grace in seconds)
            (post_final_leaderboard, "daily_final_leaderboard", 5, 32, 120),
            (post_daily_quote, "daily_quote", 5, 40, 300),
        )

        for func, job_id, hour, minute, grace in jobs:
            self.scheduler.add_job(
                func,
                trigger=CronTrigger(hour=hour, minute=minute, timezone=TIMEZONE),
                args=[self],
                id=job_id,
                replace_existing=True,
                max_instances=1,
                coalesce=True,
                misfire_grace_time=grace,
            )

    async def on_ready(self):
        log.info("Logged in as %s", self.user)


bot = TypingClubBot()


async def _send_daily_embed(ctx: commands.Context, build_embed):
    """Fetch today's data and post the embed produced by `build_embed(data)`."""
    data = await get_daily_data()

    if data is None:
        await ctx.send("Could not fetch today's competition data.")
        return

    await ctx.send(embed=build_embed(data))


@bot.command(name="daily")
async def daily(ctx: commands.Context):
    """Show today's quote."""
    await _send_daily_embed(ctx, lambda data: create_daily_quote_embed(data["quote"]))
 
 
@bot.command(name="leaderboard", aliases=["lb"])
async def leaderboard(ctx: commands.Context):
    """Show today's leaderboard."""
    await _send_daily_embed(ctx, create_daily_leaderboard_embed)



if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_TOKEN is not set.")

    bot.run(DISCORD_TOKEN)