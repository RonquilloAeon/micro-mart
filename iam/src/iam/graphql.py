import strawberry

from member import schema as member_schema


@strawberry.type
class Query:
    ...


@strawberry.type
class Mutation(member_schema.Mutation):
    ...


schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
)
