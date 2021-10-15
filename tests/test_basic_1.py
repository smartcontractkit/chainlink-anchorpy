import asyncio
from pytest import fixture, mark
from anchorpy import create_workspace, close_workspace, Context, Program
from solana.keypair import Keypair
from solana.system_program import SYS_PROGRAM_ID


@fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@mark.integration
@fixture(scope="session")
async def program() -> Program:
    workspace = create_workspace()
    yield workspace["basic_1"]
    await close_workspace(workspace)


@fixture(scope="session")
async def initialized_account(program: Program) -> Keypair:
    my_account = Keypair()
    await program.rpc["initialize"](
        1234,
        ctx=Context(
            accounts={
                "myAccount": my_account.public_key,
                "user": program.provider.wallet.public_key,
                "systemProgram": SYS_PROGRAM_ID,
            },
            signers=[my_account],
        ),
    )
    return my_account


@mark.asyncio
@mark.integration
async def test_create_and_initialize_account(
    program: Program, initialized_account: Keypair
) -> None:
    """Test creating and initializing account in single tx."""
    account = await program.account["MyAccount"].fetch(initialized_account.public_key)
    assert account["data"] == 1234


@mark.asyncio
@mark.integration
async def test_update_previously_created_account(
    initialized_account: Keypair, program: Program
) -> None:
    """Test updating a previously created account."""
    await program.rpc["update"](
        4321, ctx=Context(accounts={"myAccount": initialized_account.public_key})
    )
    account = await program.account["MyAccount"].fetch(initialized_account.public_key)
    assert account["data"] == 4321