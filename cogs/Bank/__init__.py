from .Bank import Bank

async def setup(bot):
    await bot.add_cog(Bank(bot))
