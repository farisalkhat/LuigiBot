from .Administrator import Administrator

def setup(bot):
    bot.add_cog(Administrator(bot))
