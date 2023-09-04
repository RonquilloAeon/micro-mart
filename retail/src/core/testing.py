import typing
from unittest import mock

from strawberry_django.test.client import TestClient

from adapters.streaming import EventProducer
from retail import container


class DependencyOverrideMixin:
    _mocks: dict[str, mock.Mock] = {}

    @property
    def mocks(self) -> dict[str, mock.Mock]:
        return self._mocks

    def mock_dependencies(self):
        # These mocks let us inspect dependency calls when testing
        self._mocks["event_producer"] = mock.Mock(spec=EventProducer)

        # Override the actual dependencies with our mocks
        for dep_name, mock_ in self._mocks.items():
            dep = getattr(container, dep_name)
            dep.override(mock_)

    def reset_dependencies(self):
        for dep_name in self._mocks.keys():
            del self._mocks[dep_name]

            dep = getattr(container, dep_name)
            dep.reset_override()


class GraphQlMixin:
    gql_client: typing.Optional[TestClient] = None

    def query(self, *args, **kwargs):
        if not self.gql_client:
            self.gql_client = TestClient("/graphql")

        return self.gql_client.query(*args, **kwargs)
