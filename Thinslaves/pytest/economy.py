import pytest
from Thinslaves.core import bank as bank_module

__all__ = ["bank"]


@pytest.fixture()
def bank(config, monkeypatch):
    from Thinslaves.core import Config

    with monkeypatch.context() as m:
        m.setattr(Config, "get_conf", lambda *args, **kwargs: config)
        # noinspection PyProtectedMember
        bank_module._init()
        return bank_module
