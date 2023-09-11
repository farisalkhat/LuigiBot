from .Help import Help

async def setup(bot):
    await bot.add_cog(Help(bot))
