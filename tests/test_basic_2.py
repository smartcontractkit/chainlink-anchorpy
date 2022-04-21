"""Mimics anchor/examples/tutorial/basic-2/tests/basic-2.js."""

from solana.keypair import Keypair
from solana.system_program import SYS_PROGRAM_ID

from pytest import fixture, mark
from pytest_asyncio import fixture as async_fixture
from chainlink_anchorpy import Program, Provider, Context
from chainlink_anchorpy.pytest_plugin import workspace_fixture
from chainlink_anchorpy.workspace import WorkspaceType


workspace = workspace_fixture("anchor/examples/tutorial/basic-2")


@fixture(scope="module")
def program(workspace: WorkspaceType) -> Program:
    """Create a Program instance."""
    return workspace["basic_2"]


@fixture(scope="module")
def provider(program: Program) -> Provider:
    """Get a Provider instance."""
    return program.provider


@async_fixture(scope="module")
async def created_counter(program: Program, provider: Provider) -> Keypair:
    """Create the counter."""
    counter = Keypair()
    await program.rpc["create"](
        provider.wallet.public_key,
        ctx=Context(
            accounts={
                "counter": counter.public_key,
                "user": provider.wallet.public_key,
                "system_program": SYS_PROGRAM_ID,
            },
            signers=[counter],
        ),
    )
    return counter


@mark.asyncio
async def test_create_counter(
    created_counter: Keypair,
    program: Program,
    provider: Provider,
) -> None:
    """Test creating a counter."""
    counter_account = await program.account["Counter"].fetch(created_counter.public_key)
    assert counter_account.authority == provider.wallet.public_key
    assert counter_account.count == 0


@mark.asyncio
async def test_update_counter(
    created_counter: Keypair,
    program: Program,
    provider: Provider,
) -> None:
    """Test updating the counter."""
    await program.rpc["increment"](
        ctx=Context(
            accounts={
                "counter": created_counter.public_key,
                "authority": provider.wallet.public_key,
            },
        ),
    )
    counter_account = await program.account["Counter"].fetch(created_counter.public_key)
    assert counter_account.authority == provider.wallet.public_key
    assert counter_account.count == 1
