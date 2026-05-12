from pathlib import Path
import pickle


class EmbeddingStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._data: dict[str, bytes] = {}
        if self.path.exists():
            with self.path.open("rb") as f:
                loaded = pickle.load(f)
            if not isinstance(loaded, dict):
                raise ValueError(f"store must contain dict[str, bytes], got {type(loaded)!r}")
            self._data = self._validate(loaded)

    def upsert(self, user_key: str, embedding_bytes: bytes) -> None:
        if not isinstance(user_key, str):
            raise TypeError("user_key must be str")
        if not isinstance(embedding_bytes, bytes):
            raise TypeError("embedding_bytes must be bytes")
        self._data[user_key] = embedding_bytes
        self._save()

    def all(self) -> dict[str, bytes]:
        return dict(self._data)

    def remove(self, user_key: str) -> None:
        self._data.pop(user_key, None)
        self._save()

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("wb") as f:
            pickle.dump(self._data, f)

    @staticmethod
    def _validate(data: dict[object, object]) -> dict[str, bytes]:
        validated: dict[str, bytes] = {}
        for key, value in data.items():
            if not isinstance(key, str):
                raise ValueError(f"store key must be str, got {type(key)!r}")
            if not isinstance(value, bytes):
                raise ValueError(f"store value for {key!r} must be bytes, got {type(value)!r}")
            validated[key] = value
        return validated

