# main.py is assumed to be the entry point into any extension, it must be named that.
import discord
from discord import app_commands
from discord.ext import commands
from pathlib import Path
DIR = Path(__file__).parent.absolute()

# This adds the cog to the bot
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YourCog(bot=bot))

# The cog itself
class YourCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # Define a slash command
    @app_commands.command(name="ping", description="ping pong!")
    async def channel(self, interaction: discord.Interaction):
        # Interaction object docs:
        # https://discordpy.readthedocs.io/en/stable/interactions/api.html#interaction
        await interaction.response.send_message("Pong!")

    # Define a text command
    @commands.command(name="ping")
    async def tag(self, ctx: commands.Context):
        # Context object docs:
        # https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context
        await ctx.reply("Pong!")
    
    # Define a listener
    @commands.Cog.listener()
    # Outside of a cog, this would look like `@bot.event`
    # All possible listeners:
    # https://discordpy.readthedocs.io/en/stable/api.html#event-reference
    async def on_message(self, message: discord.Message):
        # Message object docs:
        # https://discordpy.readthedocs.io/en/stable/api.html#message
        # Ignore all messages sent by the bot to prevent any recursion
        if message.author.bot: return
        
        await message.add_reaction("🐸")