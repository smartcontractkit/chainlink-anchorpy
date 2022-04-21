import json
from pathlib import Path
from pytest import mark
from chainlink_anchorpy import Idl, InstructionCoder
from chainlink_anchorpy.program.context import _check_args_length
from chainlink_anchorpy.program.common import _to_instruction  # noqa: WPS347


@mark.unit
def test_instruction_coder() -> None:
    """Test InstructionCoder behaves as expected."""
    with Path("tests/idls/basic_1.json").open() as f:
        data = json.load(f)
    idl = Idl.from_json(data)
    idl_ix = idl.instructions[0]
    args = (1234,)
    _check_args_length(idl_ix, args)
    ix = _to_instruction(idl_ix, args)
    coder = InstructionCoder(idl)
    encoded = coder.build(ix)
    assert encoded == b"\xaf\xafm\x1f\r\x98\x9b\xed\xd2\x04\x00\x00\x00\x00\x00\x00"
    assert coder.parse(encoded) == ix
