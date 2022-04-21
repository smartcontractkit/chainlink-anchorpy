"""Mimics anchor/tests/errors/tests/events.js.

Note: this is unfinished.
"""
from typing import cast
from pytest import mark, fixture
from solana.rpc.websocket_api import connect, SolanaWsClientProtocol
from solana.rpc.request_builder import LogsSubscribeFilter
from solana.rpc.responses import LogsNotification
from chainlink_anchorpy import (
    Program,
    EventParser,
)
from chainlink_anchorpy.pytest_plugin import workspace_fixture
from chainlink_anchorpy.workspace import WorkspaceType


workspace = workspace_fixture("anchor/tests/events/")


@fixture(scope="module")
def program(workspace: WorkspaceType) -> Program:
    return workspace["events"]


@mark.asyncio
async def test_initialize(program: Program) -> None:
    async with cast(SolanaWsClientProtocol, connect()) as websocket:  # type: ignore
        await websocket.logs_subscribe(LogsSubscribeFilter.ALL)
        await websocket.recv()
        await program.rpc["initialize"]()
        received = await websocket.recv()
        notification = cast(LogsNotification, received)
        logs = cast(list[str], notification.result.value.logs)
        parser = EventParser(program.program_id, program.coder)
        parsed = []
        parser.parse_logs(logs, lambda evt: parsed.append(evt))
        event = parsed[0]
        assert event.data.data == 5
        assert event.data.label == "hello"
