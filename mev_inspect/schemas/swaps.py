from typing import List, Optional

from pydantic import BaseModel

from mev_inspect.schemas.traces import Protocol

import json
from typing import List


class Swap(BaseModel):
    abi_name: str
    transaction_hash: str
    block_number: int
    trace_address: List[int]
    contract_address: str
    from_address: str
    to_address: str
    token_in_address: str
    token_in_amount: int
    token_out_address: str
    token_out_amount: int
    protocol: Optional[Protocol]
    error: Optional[str]

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toDict(self):
        return dict(self)
