from .Yugioh import Yugioh

async def setup(bot):
    await bot.add_cog(Yugioh(bot))
