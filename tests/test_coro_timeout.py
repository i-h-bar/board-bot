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


@pytest.mark.asyncio
async def test_not_timeout_args():
    @RunWithTO(timeout_s=0.1)
    async def test(arg):
        await asyncio.sleep(0.01)
        return arg

    x = 5
    result = await test(x)

    assert result
    assert result.value == x


@pytest.mark.asyncio
async def test_not_timeout_kwargs():
    @RunWithTO(timeout_s=0.1)
    async def test(arg = 6):
        await asyncio.sleep(0.01)
        return arg

    x = 5
    result = await test(arg = x)

    assert result
    assert result.value == x


@pytest.mark.asyncio
async def test_not_timeout_kwargs_default():
    @RunWithTO(timeout_s=0.1)
    async def test(arg = 6):
        await asyncio.sleep(0.01)
        return arg

    result = await test()

    assert result
    assert result.value == 6


@pytest.mark.asyncio
async def test_not_timeout_kwargs_default():
    @RunWithTO(timeout_s=0.1)
    async def test(arg, kwarg = 6):
        await asyncio.sleep(0.01)
        return arg, kwarg

    x = 5
    result = await test(5)

    assert result
    assert result.value == (x, 6)


@pytest.mark.asyncio
async def test_not_timeout_kwargs():
    @RunWithTO(timeout_s=0.1)
    async def test(arg, kwarg = 6):
        await asyncio.sleep(0.01)
        return arg, kwarg

    x = 5
    k = 4
    result = await test(5, kwarg=k)

    assert result
    assert result.value == (x, k)


@pytest.mark.asyncio
async def test_not_timeout_kwargs_pos():
    @RunWithTO(timeout_s=0.1)
    async def test(arg, kwarg = 6):
        await asyncio.sleep(0.01)
        return arg, kwarg

    x = 5
    k = 4
    result = await test(5, k)

    assert result
    assert result.value == (x, k)