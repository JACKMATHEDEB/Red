.. red commands module documentation

================
Commands Package
================

This package acts almost identically to :doc:`discord.ext.commands <dpy:ext/commands/api>`; i.e.
all of the attributes from discord.py's are also in ours. 
Some of these attributes, however, have been slightly modified, while others have been added to
extend functionlities used throughout the bot, as outlined below.

.. autofunction:: Thinslave.core.commands.command

.. autofunction:: Thinslave.core.commands.group

.. autoclass:: Thinslave.core.commands.Command
    :members:

.. autoclass:: Thinslave.core.commands.Group
    :members:

.. autoclass:: Thinslave.core.commands.Context
    :members:

.. automodule:: Thinslave.core.commands.requires
    :members: PrivilegeLevel, PermState, Requires
