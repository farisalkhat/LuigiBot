from .Economy import Economy
from .Gacha import Gacha
from .GachaEvents import GachaEvents
from .GachaBattle import GachaBattle
def setup(bot):
    bot.add_cog(Economy(bot))
    bot.add_cog(Gacha(bot))
    bot.add_cog(GachaEvents(bot))
    bot.add_cog(GachaBattle(bot))
