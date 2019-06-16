import pytest

from Thinslave.cogs.alias import Alias
from Thinslave.core import Config

__all__ = ["alias"]


@pytest.fixture()
def alias(config, monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(Config, "get_conf", lambda *args, **kwargs: config)
        return Alias(None)
