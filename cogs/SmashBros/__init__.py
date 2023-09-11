from .SmashBros import SmashBros

async def setup(bot):
    await bot.add_cog(SmashBros(bot))
