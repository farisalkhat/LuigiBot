
from .Economy import Economy
async def setup(bot):
    await bot.add_cog(Economy(bot))
    

