from .Utility import Utility

async def setup(bot):
    await bot.add_cog(Utility(bot))
