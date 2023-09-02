import typing
from unittest import mock

from microservice_utils.google_cloud.adapters.pubsub import Publisher, Subscriber
from strawberry_django.test.client import TestClient

from iam import container


class DependencyOverrideMixin:
    _mocks: dict[str, mock.Mock] = {}

    def mock_dependencies(self):
        # These mocks let us inspect dependency calls when testing
        self._mocks["publisher"] = mock.Mock(spec=Publisher)
        self._mocks["publisher"].publish.return_value = "1fe00f00800f"

        self._mocks["subscriber"] = mock.Mock(spec=Subscriber)

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
