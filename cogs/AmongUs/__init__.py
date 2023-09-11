from .AmongUs import AmongUs

async def setup(bot):
    await bot.add_cog(AmongUs(bot))
