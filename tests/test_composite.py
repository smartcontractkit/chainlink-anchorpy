"""Mimics anchor/tests/composite/tests/composite.js."""
from pytest import mark, fixture
from pytest_asyncio import fixture as async_fixture
from solana.keypair import Keypair
from solana.sysvar import SYSVAR_RENT_PUBKEY

from chainlink_anchorpy import Program, Context
from chainlink_anchorpy.workspace import WorkspaceType
from chainlink_anchorpy.pytest_plugin import workspace_fixture


workspace = workspace_fixture("anchor/tests/composite/")


@fixture(scope="module")
def program(workspace: WorkspaceType) -> Program:
    """Create a Program instance."""
    return workspace["composite"]


@async_fixture(scope="module")
async def initialized_accounts(program: Program) -> tuple[Keypair, Keypair]:
    """Generate keypairs and use them when callling the initialize function."""
    dummy_a = Keypair()
    dummy_b = Keypair()
    await program.rpc["initialize"](
        ctx=Context(
            accounts={
                "dummy_a": dummy_a.public_key,
                "dummy_b": dummy_b.public_key,
                "rent": SYSVAR_RENT_PUBKEY,
            },
            signers=[dummy_a, dummy_b],
            pre_instructions=[
                await program.account["DummyA"].create_instruction(dummy_a),
                await program.account["DummyB"].create_instruction(dummy_b),
            ],
        ),
    )
    return dummy_a, dummy_b


@async_fixture(scope="module")
async def composite_updated_accounts(
    program: Program,
    initialized_accounts: tuple[Keypair, Keypair],
) -> tuple[Keypair, Keypair]:
    """Run composite_update and return the keypairs used."""
    dummy_a, dummy_b = initialized_accounts
    ctx = Context(
        accounts={
            "foo": {"dummy_a": dummy_a.public_key},
            "bar": {"dummy_b": dummy_b.public_key},
        },
    )
    await program.rpc["composite_update"](1234, 4321, ctx=ctx)
    return initialized_accounts


@mark.asyncio
async def test_composite_update(
    program: Program,
    composite_updated_accounts: tuple[Keypair, Keypair],
) -> None:
    """Test that the call to composite_update worked."""
    dummy_a, dummy_b = composite_updated_accounts
    dummy_a_account = await program.account["DummyA"].fetch(dummy_a.public_key)
    dummy_b_account = await program.account["DummyB"].fetch(dummy_b.public_key)
    assert dummy_a_account.data == 1234
    assert dummy_b_account.data == 4321
