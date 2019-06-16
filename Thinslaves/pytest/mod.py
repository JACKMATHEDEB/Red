import pytest
from Thinslaves.core import modlog

__all__ = ["mod"]


@pytest.fixture
def mod(config, monkeypatch):
    from Thinslaves.core import Config

    with monkeypatch.context() as m:
        m.setattr(Config, "get_conf", lambda *args, **kwargs: config)

        modlog._init()
        return modlog
