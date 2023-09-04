import typing

import typesense


class TypesenseSearch:
    def __init__(
        self,
        api_key: str,
        host: str,
        port: str,
        protocol: typing.Optional[typing.Literal["http", "https"]] = "http",
    ) -> None:
        self._client = typesense.Client(
            {
                "nodes": [
                    {
                        "host": host,
                        "port": port,
                        "protocol": protocol,
                    }
                ],
                "api_key": api_key,
                "connection_timeout_seconds": 5,
            }
        )

    @property
    def collections(self):
        return self._client.collections

    def add(self, collection: str, document: dict):
        self.collections[collection].documents.upsert(document)

    def batch_add(self, collection: str, documents: list[str]):
        self.collections[collection].documents.import_(documents)

    def create_collection(self, schema: dict) -> str:
        # TODO aliasing
        self._client.collections.create(schema)

        return schema["name"]
