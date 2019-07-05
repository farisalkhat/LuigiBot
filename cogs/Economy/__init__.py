from .Economy import Economy
from .NewEconomy import NewEconomy
def setup(bot):
    bot.add_cog(Economy(bot))
    bot.add_cog(NewEconomy(bot))
    

