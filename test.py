from mev_inspect.db import get_inspect_session, get_trace_session
from mev_inspect.inspector import MEVInspector
import asyncio
inspect_db_session = get_inspect_session()
trace_db_session = get_trace_session()
rpc = "http://128.59.19.217:9991"
geth = True
inspector = MEVInspector(rpc, inspect_db_session, trace_db_session, geth)


async def main():
    results = []
    after_block = 100
    before_block = 200
    await inspector.inspect_many_blocks(
        after_block=after_block,
        before_block=before_block
    )
asyncio.run(main())
