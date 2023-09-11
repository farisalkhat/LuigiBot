from .Administrator import Administrator

async def setup(bot):
    await bot.add_cog(Administrator(bot))
