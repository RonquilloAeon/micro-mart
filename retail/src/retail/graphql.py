import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from product import schema as product_schema


@strawberry.type
class Query(product_schema.Query):
    ...


# @strawberry.type
# class Mutation(product_schema.Mutation):
#     ...


schema = strawberry.federation.Schema(
    query=Query,
    # mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
