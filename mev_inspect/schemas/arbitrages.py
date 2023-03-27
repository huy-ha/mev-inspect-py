from typing import List

from pydantic import BaseModel

from .swaps import Swap
import json


class Arbitrage(BaseModel):
    swaps: List[Swap]
    block_number: int
    transaction_hash: str
    account_address: str
    profit_token_address: str
    start_amount: int
    end_amount: int
    profit_amount: int

    def toJson(self):
        return json.dumps(dict(
            swaps=list(map(lambda x: x.toDict(), self.swaps)),
            block_number=self.block_number,
            transaction_hash=self.transaction_hash,
            account_address=self.account_address,
            profit_token_address=self.profit_token_address,
            start_amount=self.start_amount,
            end_amount=self.end_amount,
            profit_amount=self.profit_amount,
        ))
