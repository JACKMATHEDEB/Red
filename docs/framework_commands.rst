.. red commands module documentation

================
Commands Package
================

This package acts almost identically to :doc:`discord.ext.commands <dpy:ext/commands/api>`; i.e.
all of the attributes from discord.py's are also in ours. 
Some of these attributes, however, have been slightly modified, while others have been added to
extend functionlities used throughout the bot, as outlined below.

.. autofunction:: Thinslaves.core.commands.command

.. autofunction:: Thinslaves.core.commands.group

.. autoclass:: Thinslaves.core.commands.Command
    :members:

.. autoclass:: Thinslaves.core.commands.Group
    :members:

.. autoclass:: Thinslaves.core.commands.Context
    :members:

.. automodule:: Thinslaves.core.commands.requires
    :members: PrivilegeLevel, PermState, Requires
