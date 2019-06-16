from unittest.mock import MagicMock

import pytest

from Thinslave.cogs.admin import Admin
from Thinslave.cogs.admin.announcer import Announcer

__all__ = ["admin", "announcer"]


@pytest.fixture()
def admin(config):
    return Admin(config)


@pytest.fixture()
def announcer(admin):
    a = Announcer(MagicMock(), "Some message", admin.conf)
    yield a
    a.cancel()
