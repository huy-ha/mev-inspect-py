from pathlib import Path
from typing import List
from mev_inspect.schemas import receipts

from web3 import Web3

from mev_inspect.fees import fetch_base_fee_per_gas
from mev_inspect.geth import geth_get_tx_traces, geth_trace_translator
from mev_inspect.geth import geth_get_tx_receipts, geth_receipts_translator
from mev_inspect.schemas import Block, Trace, TraceType
from mev_inspect.schemas.receipts import Receipt


cache_directory = "./cache"


def create_from_block_number(
    base_provider, w3: Web3, block_number: int, should_cache: bool, nodetype: str
) -> Block:
    if not should_cache:
        return fetch_block(w3, base_provider, block_number, nodetype)

    cache_path = _get_cache_path(block_number)

    if cache_path.is_file():
        print(f"Cache for block {block_number} exists, " "loading data from cache")

        return Block.parse_file(cache_path)
    else:
        print(f"Cache for block {block_number} did not exist, getting data")

        block = fetch_block(w3, base_provider, block_number, nodetype)

        cache_block(cache_path, block)

        return block

def fetch_block_geth(w3: Web3, base_provider, block_number: int) -> Block:
    block_json = w3.eth.get_block(block_number)
    # print("got block json ", block_json)

    geth_tx_traces = geth_get_tx_traces(base_provider, block_json['transactions'])
    geth_tx_receipts = geth_get_tx_receipts(base_provider, block_json['transactions'])
    print("Got geth traces and receipts", len(geth_tx_traces), len(geth_tx_receipts))

    parity_block_traces = geth_trace_translator(block_json, geth_tx_traces)
    parity_receipts = geth_receipts_translator(block_json, geth_tx_receipts)
    print("Translated parity traces and receipts", len(parity_block_traces), len(parity_receipts))

    return Block(
        block_number=block_number,
        miner=block_json["miner"], #TODO: Polygon miners are 0x000 ?
        base_fee_per_gas=0, #TODO
        traces = parity_block_traces,
        receipts=parity_receipts,
    )

def fetch_block_parity(w3: Web3, base_provider, block_number: int) -> Block:
    block_json = w3.eth.get_block(block_number)
    receipts_json = base_provider.make_request("eth_getBlockReceipts", [block_number])
    traces_json = w3.parity.trace_block(block_number)

    receipts: List[Receipt] = [
        Receipt(**receipt) for receipt in receipts_json["result"]
    ]
    traces = [Trace(**trace_json) for trace_json in traces_json]
    base_fee_per_gas = fetch_base_fee_per_gas(w3, block_number)

    return Block(
        block_number=block_number,
        miner=block_json["miner"],
        base_fee_per_gas=base_fee_per_gas,
        traces=traces,
        receipts=receipts,
    )

def fetch_block(w3, base_provider, block_number: int, nodetype: str) -> Block:
    if nodetype == "geth":
        # print("fetching geth block")
        return fetch_block_geth(w3, base_provider, block_number)
    elif nodetype == "parity":
        return fetch_block_parity(w3, base_provider, block_number)


def get_transaction_hashes(calls: List[Trace]) -> List[str]:
    result = []

    for call in calls:
        if call.type != TraceType.reward:
            if (
                call.transaction_hash is not None
                and call.transaction_hash not in result
            ):
                result.append(call.transaction_hash)

    return result


def cache_block(cache_path: Path, block: Block):
    write_mode = "w" if cache_path.is_file() else "x"

    with open(cache_path, mode=write_mode) as cache_file:
        cache_file.write(block.json())


def _get_cache_path(block_number: int) -> Path:
    cache_directory_path = Path(cache_directory)
    return cache_directory_path / f"{block_number}-new.json"
