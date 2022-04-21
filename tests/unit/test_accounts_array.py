from chainlink_anchorpy import Idl
from pathlib import Path
from pytest import mark
import json
from solana.keypair import Keypair
from solana.transaction import AccountMeta

from chainlink_anchorpy.program.namespace.instruction import _accounts_array


@mark.unit
def test_accounts_array() -> None:
    """Test accounts_array returns expected."""
    with Path("tests/idls/composite.json").open() as f:
        idl_json = json.load(f)
    idl = Idl.from_json(idl_json)
    dummy_a = Keypair.generate()
    dummy_b = Keypair.generate()
    comp_accounts = {
        "foo": {
            "dummy_a": dummy_a.public_key,
        },
        "bar": {
            "dummy_b": dummy_b.public_key,
        },
    }
    accounts_arg = idl.instructions[1].accounts
    acc_arr = _accounts_array(comp_accounts, accounts_arg)
    assert acc_arr == [
        AccountMeta(pubkey=dummy_a.public_key, is_signer=False, is_writable=True),
        AccountMeta(pubkey=dummy_b.public_key, is_signer=False, is_writable=True),
    ]
