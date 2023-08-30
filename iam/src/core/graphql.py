import typing

import strawberry
from strawberry.scalars import JSON

from .services import ServiceResult


@strawberry.type
class Error:
    message: str


@strawberry.type
class MutationResult:
    success: bool
    entities: list[JSON]
    errors: typing.Optional[str]


def convert_service_result_to_mutation_result(
    service_result: ServiceResult,
) -> MutationResult:
    return MutationResult(
        entities=service_result.entities,
        errors=[Error(message=error.message) for error in service_result.errors],
        success=service_result.success,
    )
