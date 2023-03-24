from db import DB

class CacheKeys:
	class UTXO(DB.Key):
		def __init__(self, txid: str, vout: int) -> None:
			self._bytes = f'utxo-{txid}-{vout}'.encode('ascii')
		
		def bytes(self) -> bytes:
			return self._bytes

	class STXO(DB.Key):
		def __init__(self, output_txid: str, vout: int) -> None:
			self._bytes = f'stxo-{output_txid}-{vout}'.encode('ascii')
		
		def bytes(self) -> bytes:
			return self._bytes

	class SatSeconds(DB.Key):
		def __init__(self, block_hash: str) -> None:
			self._bytes = f'satseconds-{block_hash}'.encode('ascii')
		
		def bytes(self) -> bytes:
			return self._bytes
