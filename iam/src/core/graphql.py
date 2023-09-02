import strawberry
from strawberry.scalars import JSON

from .services import ServiceResult


@strawberry.type
class Error:
    message: str


@strawberry.type
class Entity:
    id: str
    name: str
    data: JSON


@strawberry.type
class MutationResult:
    success: bool
    entities: list[Entity]
    errors: list[Error]


def convert_service_result_to_mutation_result(
    service_result: ServiceResult,
) -> MutationResult:
    entities = []

    for entity in service_result.entities:
        entities.append(Entity(id=entity.id, name=entity.name, data=entity.data))

    return MutationResult(
        entities=entities,
        errors=[Error(message=error.message) for error in service_result.errors],
        success=service_result.success,
    )
