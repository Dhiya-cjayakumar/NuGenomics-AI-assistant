import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

@pytest.fixture(autouse=True)
def mock_vertex(monkeypatch):
    class _FakeEvent:
        def __init__(self, text):
            self._text = text
        def is_final_response(self):
            return True
        @property
        def content(self):
            class _C:
                parts = [type("P", (), {"text": self._text})()]
            return _C()

    async def _fake_run_async(*args, **kwargs):
        yield _FakeEvent("Mock wellness answer")

    monkeypatch.setattr(
        "app.agents.wellness_agent.runner.run_async",
        _fake_run_async
    )

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()
