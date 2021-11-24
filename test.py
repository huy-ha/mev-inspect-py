from mev_inspect.db import get_inspect_session, get_trace_session
from mev_inspect.inspector import MEVInspector
import asyncio
inspect_db_session = get_inspect_session()
trace_db_session = get_trace_session()
rpc = "http://localhost:9991"
geth = True
inspector = MEVInspector(rpc, inspect_db_session, trace_db_session, geth)
block_number = 10
asyncio.run(inspector.inspect_single_block(block=block_number))
