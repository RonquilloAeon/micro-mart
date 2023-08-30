import typing
from unittest import mock

from microservice_utils.google_cloud.adapters.pubsub import Publisher, Subscriber

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
