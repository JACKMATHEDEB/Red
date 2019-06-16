from .alias import Alias
from Thinslaves.core.bot import Red


def setup(bot: Red):
    bot.add_cog(Alias(bot))
