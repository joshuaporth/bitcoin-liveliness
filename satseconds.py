import sys
from os import path
from db import DB
from cache import Cache

from blockchain_parser.blockchain import get_files, get_blocks
from blockchain_parser.block import Block
from tqdm import tqdm

# Running an umbrel node so the blocks aren't in the typical directory
BLOCKS_DIR = "~/umbrel/app-data/bitcoin/data/bitcoin/blocks"

# Maximum number of blocks to process. Set to 0 to ignore
MAX_BLOCKS = 200_000

# Maximum number of bytes a cache can store in memory before we flush to disk
MAX_BYTES_PER_CACHE = 2 * 1_073_741_824

# For UTXOs we need to store the output's value and timestamp of the block
class UTXO:
    def __init__(self, blocktime: int, value: int) -> None:
        self.blocktime = blocktime
        self.value = value


# For STXOs we only need the timestamp of the block since the redeemed output contains the value
class STXO:
    def __init__(self, blocktime: int) -> None:
        self.blocktime = blocktime


# Sat Seconds Destroyed = value(Sats) * lifespan(S)
class SatSeconds:
    def __init__(self, destroyed_on: int, last_spent: int, value: int) -> None:
        self.destroyed_on = destroyed_on
        self.sat_seconds = (destroyed_on - last_spent) * value


class CacheKey(DB.Key):
    def __init__(self, type: type, tx_hash: str, tx_idx: int) -> None:
        self.key = f"{type.__name__}_{tx_hash}_{tx_idx}"

    def bytes(self) -> bytes:
        return self.key.encode()


txo_cache = Cache[UTXO | STXO]("db/cache/")
data = Cache[SatSeconds]("db/data/")

try:
    num_blocks = 0
    blk_files = get_files(path.expanduser(BLOCKS_DIR))
    for blk_file in tqdm(blk_files):
        for raw_block in get_blocks(blk_file):
            block = Block(raw_block)
            blocktime = int(block.header.timestamp.timestamp())

            for tx in block.transactions:
                # Check if we've seen the UTXOs being redeemed in this transaction
                # If so, note the SSD and delete the redeemed UTXO, otherwise cache the STXO
                for _, input in enumerate(tx.inputs):
                    tx_hash = input.transaction_hash
                    i = input.transaction_index
                    utxo_key = CacheKey(UTXO, tx_hash, i)
                    utxo: UTXO = txo_cache.get(utxo_key)
                    if utxo:
                        satseconds_key = CacheKey(SatSeconds, tx_hash, i)
                        satseconds = SatSeconds(blocktime, utxo.blocktime, utxo.value)
                        data.put(satseconds_key, satseconds)
                        txo_cache.delete(utxo_key)
                    else:
                        stxo_key = CacheKey(STXO, tx_hash, i)
                        stxo = STXO(blocktime)
                        txo_cache.put(stxo_key, stxo)

                # Check if we've seen STXOs for the outputs in this transaction
                # If so, not the SSD and delete the STXO, otherwise cache the UTXO
                for i, output in enumerate(tx.outputs):
                    stxo_key = CacheKey(STXO, tx.hash, i)
                    stxo: STXO = txo_cache.get(stxo_key)
                    if stxo:
                        satseconds_key = CacheKey(SatSeconds, tx.hash, i)
                        satseconds = SatSeconds(stxo.blocktime, blocktime, output.value)
                        data.put(satseconds_key, satseconds)
                        txo_cache.delete(stxo_key)
                    else:
                        utxo_key = CacheKey(UTXO, tx.hash, i)
                        utxo = UTXO(blocktime, output.value)
                        txo_cache.put(utxo_key, utxo)

            num_blocks += 1
            if num_blocks == MAX_BLOCKS:
                sys.stdout.write("MAX_BLOCKS reached. Exiting now.")
                sys.exit(0)

        # Check if the cache sizes meet or exceed the limit and flush to disk if needed
        if txo_cache.size() >= MAX_BYTES_PER_CACHE:
            txo_cache.flush()
        if data.size() >= MAX_BYTES_PER_CACHE:
            data.flush()

finally:
    # Make sure the caches are clear before we exit
    txo_cache.flush()
    data.flush()
