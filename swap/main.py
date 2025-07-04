from web3 import Web3
from decimal import Decimal
from pydantic import BaseModel

w3          = Web3(Web3.HTTPProvider(os.getenv("RPC_URL", "https://rpc.fadaka.network")))
SWAP_PRIVKY = os.getenv("SWAP_SIGNER_KEY")           # cold signer key
SWAP_ROUTER = os.getenv("SWAP_ROUTER")               # same as front‑end addr
ROUTER_ABI  = json.loads(os.getenv("ROUTER_ABI_JSON","[]"))

router      = w3.eth.contract(address=SWAP_ROUTER, abi=ROUTER_ABI)
acct        = w3.eth.account.from_key(SWAP_PRIVKY)

class SwapReq(BaseModel):
    amount: Decimal          # FDAK amount (18 dp)
    to: str                  # user address

@app.post("/swap")
def backend_swap(q: SwapReq):
    if not w3.is_address(q.to):
        raise HTTPException(400, "Bad address")
    amount_wei = int(q.amount * (10 ** 18))
    tx         = router.functions.swap(amount_wei).build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 150_000,
        "gasPrice": w3.eth.gas_price,
    })
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return {"hash": tx_hash.hex()}
