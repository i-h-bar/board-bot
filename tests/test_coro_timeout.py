import asyncio

import pytest

from utils.coro_timeout import RunWithTO


@pytest.mark.asyncio
async def test_timeout():
    @RunWithTO(timeout_s=0.1)
    async def test():
        await asyncio.sleep(5)

    result = await test()

    assert not result


@pytest.mark.asyncio
async def test_not_timeout():
    @RunWithTO(timeout_s=0.1)
    async def test():
        await asyncio.sleep(0.01)
        return "value"

    result = await test()

    assert result
    assert result.value == "value"
