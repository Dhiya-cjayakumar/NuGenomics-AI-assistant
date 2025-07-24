import pytest
from app.agents.wellness_agent import arun

@pytest.mark.asyncio
async def test_wellness_mock():
    response = await arun("What are genetic markers?")
    assert "Mock wellness answer" in response
