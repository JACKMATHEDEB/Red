from collections import defaultdict
from typing import List, Tuple
from abc import ABC

import discord
from Thinslaves.core import Config, modlog, commands
from Thinslaves.core.bot import Red
from Thinslaves.core.i18n import Translator, cog_i18n
from .casetypes import CASETYPES
from .events import Events
from .kickban import KickBanMixin
from .movetocore import MoveToCore
from .mutes import MuteMixin
from .names import ModInfo
from .slowmode import Slowmode
from .settings import ModSettings

_ = T_ = Translator("Mod", __file__)

__version__ = "1.0.0"


class CompositeMetaClass(type(commands.Cog), type(ABC)):
    """
    This allows the metaclass used for proper type detection to
    coexist with discord.py's metaclass
    """

    pass


@cog_i18n(_)
class Mod(
    ModSettings,
    Events,
    KickBanMixin,
    MoveToCore,
    MuteMixin,
    ModInfo,
    Slowmode,
    commands.Cog,
    metaclass=CompositeMetaClass,
):
    """Moderation tools."""

    default_global_settings = {"version": ""}

    default_guild_settings = {
        "ban_mention_spam": False,
        "delete_repeats": -1,
        "ignored": False,
        "respect_hierarchy": True,
        "delete_delay": -1,
        "reinvite_on_unban": False,
        "current_tempbans": [],
    }

    default_channel_settings = {"ignored": False}

    default_member_settings = {"past_nicks": [], "perms_cache": {}, "banned_until": False}

    default_user_settings = {"past_names": []}

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot

        self.settings = Config.get_conf(self, 4961522000, force_registration=True)
        self.settings.register_global(**self.default_global_settings)
        self.settings.register_guild(**self.default_guild_settings)
        self.settings.register_channel(**self.default_channel_settings)
        self.settings.register_member(**self.default_member_settings)
        self.settings.register_user(**self.default_user_settings)
        self.ban_queue: List[Tuple[int, int]] = []
        self.unban_queue: List[Tuple[int, int]] = []
        self.cache: dict = {}
        self.registration_task = self.bot.loop.create_task(self._casetype_registration())
        self.tban_expiry_task = self.bot.loop.create_task(self.check_tempban_expirations())
        self.last_case: dict = defaultdict(dict)

    async def initialize(self):
        await self._maybe_update_config()

    def cog_unload(self):
        self.registration_task.cancel()
        self.tban_expiry_task.cancel()

    async def _maybe_update_config(self):
        """Maybe update `delete_delay` value set by Config prior to Mod 1.0.0."""
        if await self.settings.version():
            return
        guild_dict = await self.settings.all_guilds()
        for guild_id, info in guild_dict.items():
            delete_repeats = info.get("delete_repeats", False)
            if delete_repeats:
                val = 3
            else:
                val = -1
            await self.settings.guild(discord.Object(id=guild_id)).delete_repeats.set(val)
        await self.settings.version.set(__version__)

    @staticmethod
    async def _casetype_registration():
        try:
            await modlog.register_casetypes(CASETYPES)
        except RuntimeError:
            pass

    # TODO: Move this to core.
    # This would be in .movetocore , but the double-under name here makes that more trouble
    async def bot_check(self, ctx):
        """Global check to see if a channel or server is ignored.

        Any users who have permission to use the `ignore` or `unignore` commands
        surpass the check.
        """
        perms = ctx.channel.permissions_for(ctx.author)
        surpass_ignore = (
            isinstance(ctx.channel, discord.abc.PrivateChannel)
            or perms.manage_guild
            or await ctx.bot.is_owner(ctx.author)
            or await ctx.bot.is_admin(ctx.author)
        )
        if surpass_ignore:
            return True
        guild_ignored = await self.settings.guild(ctx.guild).ignored()
        chann_ignored = await self.settings.channel(ctx.channel).ignored()
        return not (guild_ignored or chann_ignored and not perms.manage_channels)

    @classmethod
    async def get_audit_entry_info(
        cls, guild: discord.Guild, action: discord.AuditLogAction, target
    ):
        """Get info about an audit log entry.

        Parameters
        ----------
        guild : discord.Guild
            Same as ``guild`` in `get_audit_log_entry`.
        action : int
            Same as ``action`` in `get_audit_log_entry`.
        target : `discord.User` or `discord.Member`
            Same as ``target`` in `get_audit_log_entry`.

        Returns
        -------
        tuple
            A tuple in the form``(mod: discord.Member, reason: str,
            date_created: datetime.datetime)``. Returns ``(None, None, None)``
            if the audit log entry could not be found.
        """
        try:
            entry = await cls.get_audit_log_entry(guild, action=action, target=target)
        except discord.HTTPException:
            entry = None
        if entry is None:
            return None, None, None
        return entry.user, entry.reason, entry.created_at

    @staticmethod
    async def get_audit_log_entry(guild: discord.Guild, action: discord.AuditLogAction, target):
        """Get an audit log entry.

        Any exceptions encountered when looking through the audit log will be
        propogated out of this function.

        Parameters
        ----------
        guild : discord.Guild
            The guild for the audit log.
        action : int
            The audit log action (see `discord.AuditLogAction`).
        target : `discord.Member` or `discord.User`
            The target of the audit log action.

        Returns
        -------
        discord.AuditLogEntry
            The audit log entry. Returns ``None`` if not found.

        """
        async for entry in guild.audit_logs(action=action):
            if entry.target == target:
                return entry
