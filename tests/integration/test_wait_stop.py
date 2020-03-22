import asyncio

import pytest

from procrastinate import app
from procrastinate import worker as worker_module


@pytest.mark.asyncio
async def test_wait_for_activity(pg_connector):
    """
    Testing that a new event interrupts the wait
    """
    pg_app = app.App(connector=pg_connector)
    worker = worker_module.Worker(app=pg_app, timeout=2)
    task = asyncio.ensure_future(worker.single_worker())
    await asyncio.sleep(0.2)  # should be enough so that we're waiting

    worker.stop_requested = True
    worker.notify_event.set()

    try:
        await asyncio.wait_for(task, timeout=0.2)
    except asyncio.TimeoutError:
        pytest.fail("Failed to stop worker within .2s")


@pytest.mark.asyncio
async def test_wait_for_activity_timeout(pg_connector):
    """
    Testing that we timeout if nothing happens
    """
    pg_app = app.App(connector=pg_connector)
    worker = worker_module.Worker(app=pg_app, timeout=2)
    task = asyncio.ensure_future(worker.single_worker())
    try:
        await asyncio.sleep(0.2)  # should be enough so that we're waiting

        worker.stop_requested = True

        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(task, timeout=0.2)
    finally:
        worker.notify_event.set()


@pytest.mark.asyncio
async def test_wait_for_activity_stop_from_signal(pg_connector, kill_own_pid):
    """
    Testing than ctrl+c interrupts the wait
    """
    pg_app = app.App(connector=pg_connector)
    worker = worker_module.Worker(app=pg_app, timeout=2)
    task = asyncio.ensure_future(worker.run())
    await asyncio.sleep(0.2)  # should be enough so that we're waiting

    kill_own_pid()

    try:
        await asyncio.wait_for(task, timeout=0.2)
    except asyncio.TimeoutError:
        pytest.fail("Failed to stop worker within .2s")


@pytest.mark.asyncio
async def test_wait_for_activity_stop(pg_connector):
    """
    Testing than calling job_store.stop() interrupts the wait
    """
    pg_app = app.App(connector=pg_connector)
    worker = worker_module.Worker(app=pg_app, timeout=2)
    task = asyncio.ensure_future(worker.run())
    await asyncio.sleep(0.2)  # should be enough so that we're waiting

    worker.stop()

    try:
        await asyncio.wait_for(task, timeout=0.2)
    except asyncio.TimeoutError:
        pytest.fail("Failed to stop worker within .2s")
