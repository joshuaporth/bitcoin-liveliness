import pickle
import plyvel

class DB:
	class Key:
		def __init__(self) -> None:
			pass

		def bytes(self) -> bytes:
			pass

		def __eq__(self, other: object) -> bool:
			return self.bytes() == other.bytes()
		
		def __hash__(self) -> int:
			return self.bytes().__hash__()

	def __init__(self, db_dir: str) -> None:
		self._db = plyvel.DB(db_dir, create_if_missing=True)
	
	def get(self, key: Key) -> any:
		data = self._db.get(key.bytes())
		if data:
			return pickle.loads(data)
		return None

	def batch(self, puts: list[tuple[Key, any]], deletes: list[Key]) -> None:
		with self._db.write_batch() as wb:
			for key, data in puts:
				wb.put(key.bytes(), pickle.dumps(data))
			for key in deletes:
				wb.delete(key.bytes())
