import strawberry
from strawberry.relay.utils import to_base64
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
        global_id = to_base64(entity.name, entity.id)
        entities.append(Entity(id=global_id, name=entity.name, data=entity.data))

    return MutationResult(
        entities=entities,
        errors=[Error(message=error.message) for error in service_result.errors],
        success=service_result.success,
    )
