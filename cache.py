import sys
from typing import TypeVar, Generic
from db import DB

T = TypeVar("T")

class Cache(Generic[T]):
	def __init__(self, cache_dir: str) -> None:
		self._db = DB(cache_dir)
		self._puts: dict[DB.Key, T] = {}
		self._deletes: list[DB.Key] = []
	
	def get(self, key: DB.Key) -> T:
		if key in self._puts:
			return self._puts[key]
		else:
			return self._db.get(key)

	def put(self, key: DB.Key, data: T) -> None:
		self._puts[key] = data
	
	def delete(self, key: DB.Key) -> None:
		if key in self._puts:
			del self._puts[key]
		else:
			self._deletes.append(key)
	
	def flush(self) -> None:
		puts = list(self._puts.items())
		self._db.batch(puts, self._deletes)
		self._puts.clear()
		self._deletes.clear()
	
	def size(self) -> int:
		return sys.getsizeof(self._puts) + sys.getsizeof(self._deletes)