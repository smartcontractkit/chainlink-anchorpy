from pathlib import Path
import json
from chainlink_anchorpy import EventParser, Idl, Program, Event
from solana.publickey import PublicKey


def test_event_parser() -> None:
    path = Path("tests/idls/jet.json")
    with path.open() as f:
        data = json.load(f)
    idl = Idl.from_json(data)
    program = Program(idl, PublicKey("JPv1rCqrhagNNmJVM5J1he7msQ5ybtvE1nNuHpDHMNU"))
    logs = [
        "Program 11111111111111111111111111111111 invoke [1]",
        "Program 11111111111111111111111111111111 success",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [1]",
        "Program log: Instruction: InitializeAccount",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 3680 of 200000 compute units",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
        "Program JPv1rCqrhagNNmJVM5J1he7msQ5ybtvE1nNuHpDHMNU invoke [1]",
        "Program log: reserve refreshed",
        "Program JPv1rCqrhagNNmJVM5J1he7msQ5ybtvE1nNuHpDHMNU consumed 22613 of 200000 compute units",
        "Program JPv1rCqrhagNNmJVM5J1he7msQ5ybtvE1nNuHpDHMNU success",
        "Program JPv1rCqrhagNNmJVM5J1he7msQ5ybtvE1nNuHpDHMNU invoke [1]",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
        "Program log: Instruction: Transfer",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 3229 of 187213 compute units",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
        "Program log: Instruction: MintTo",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 2883 of 181487 compute units",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
        "Program JPv1rCqrhagNNmJVM5J1he7msQ5ybtvE1nNuHpDHMNU consumed 22300 of 200000 compute units",
        "Program JPv1rCqrhagNNmJVM5J1he7msQ5ybtvE1nNuHpDHMNU success",
        "Program JPv1rCqrhagNNmJVM5J1he7msQ5ybtvE1nNuHpDHMNU invoke [1]",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
        "Program log: Instruction: Transfer",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 3121 of 186053 compute units",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
        "Program log: qQ5mlJuJEus/bRqvmKjiBjRyfYn7cnNNHT77Kz7sKsqij6V2ExQ1ZU96Ui/iFPUsyTUAU3mfJA59v/QuP96VXE0+zTvStnmOAACUNXcAAAAA",
        "Program JPv1rCqrhagNNmJVM5J1he7msQ5ybtvE1nNuHpDHMNU consumed 20763 of 200000 compute units",
        "Program JPv1rCqrhagNNmJVM5J1he7msQ5ybtvE1nNuHpDHMNU success",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [1]",
        "Program log: Instruction: CloseAccount",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 2160 of 200000 compute units",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
    ]
    parser = EventParser(program.program_id, program.coder)
    evts = []
    parser.parse_logs(logs, lambda evt: evts.append(evt))
    events_coder = program.coder.events
    event_cls = events_coder.layouts["DepositCollateralEvent"].datacls  # type: ignore
    expected_data = event_cls(
        depositor=PublicKey("5GbBHT4CCQsmbP2oLscHtRZsNdsj3Y1mrbMSiLSE4Jpt"),
        reserve=PublicKey("6MFPbC1VvuHTH99X1jdSpxw9kdNA7ZdsmzQgJy4cTsNd"),
        amount=program.type["Amount"](
            units=program.type["AmountUnits"].Tokens(), value=2000000000
        ),
    )
    expected_event = Event(name="DepositCollateralEvent", data=expected_data)
    assert len(evts) == 1
    assert str(evts[0]) == str(expected_event)
