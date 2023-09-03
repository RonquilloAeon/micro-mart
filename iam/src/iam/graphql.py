import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from member import schema as member_schema


@strawberry.type
class Query(member_schema.Query):
    ...


@strawberry.type
class Mutation(member_schema.Mutation):
    ...


schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
