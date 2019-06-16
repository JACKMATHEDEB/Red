from .filter import Filter
from Thinslave.core.bot import Red


def setup(bot: Red):
    bot.add_cog(Filter(bot))
