import logging
import typing
from dataclasses import dataclass, field

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from functools import wraps

logger = logging.getLogger("django")


@dataclass
class Error:
    message: str


@dataclass
class Entity:
    id: typing.Any
    name: str
    data: typing.Optional[dict] = field(default_factory=dict)


@dataclass
class ServiceResult:
    errors: list[Error] = field(default_factory=list)
    entities: list[Entity] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return not bool(self.errors)

    def add_error(self, message: str) -> None:
        self.errors.append(Error(message))

    def add_entity(
        self,
        entity: typing.Any,
        data_attributes: typing.Optional[list[str]] = None,
        entity_id_attribute: str = "id",
    ) -> None:
        id_ = getattr(entity, entity_id_attribute, None)
        name = entity.__class__.__name__

        if data_attributes:
            data = {attr: getattr(entity, attr, None) for attr in data_attributes}
        else:
            data = {}

        self.entities.append(Entity(id_, name, data))


T = typing.TypeVar("T")
P = typing.ParamSpec("P")

UserFriendlyMessage: typing.TypeAlias = str
Exceptions = dict[typing.Type[Exception], UserFriendlyMessage]

_SYSTEM_EXCEPTIONS = {
    Exception: "Oops! Something went wrong.",
    ObjectDoesNotExist: "Can't find the requested entity.",
}

_BUSINESS_EXCEPTIONS = {
    PermissionDenied: "Sorry, you can't do this.",
}

_DEFAULT_EXCEPTIONS = {**_SYSTEM_EXCEPTIONS, **_BUSINESS_EXCEPTIONS}


def execute_safely(
    fn: typing.Callable[P, T] = None, *, exceptions: Exceptions = None
) -> typing.Callable[P, T]:
    """Decorator for services that catches and handles exceptions, preventing them from propagating to controllers.
    It uses an extendable registry to map exceptions to error messages."""

    if not exceptions:
        exceptions = {}

    def exception_handling_wrapper(fn: typing.Callable[P, T]):
        @wraps(fn)
        def _wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                exception_message = str(e)

                logger.warning("Caught service exception: %s", exception_message)
                logger.exception("Service exception is being handled. ")

                all_exceptions = {**_DEFAULT_EXCEPTIONS, **exceptions}
                service_result = ServiceResult()

                try:
                    # If the exception is not in our mapping, a KeyError will be raised.
                    service_result.add_error(all_exceptions[e.__class__])
                except KeyError as e:
                    service_result.add_error(all_exceptions[Exception])

                    logger.debug("Unexpected service exception: %s", e)
                    logger.exception("An unexpected service exception was caught. ")

                return service_result

        return _wrapper

    if fn:
        return exception_handling_wrapper(fn)
    else:
        return exception_handling_wrapper
