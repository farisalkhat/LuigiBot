from .Dota import Dota

async def setup(bot):
    await bot.add_cog(Dota(bot))
