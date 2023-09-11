from .DrWilyDB import DrWilyDB

async def setup(bot):
   await bot.add_cog(DrWilyDB(bot))
