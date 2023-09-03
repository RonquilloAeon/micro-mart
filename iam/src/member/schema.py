import typing
from uuid import UUID

import strawberry
from strawberry import relay
import strawberry_django

from core.graphql import MutationResult, convert_service_result_to_mutation_result
from member import models as member_models
from member.services import MemberData, RegisterMemberService


@strawberry_django.type(member_models.Member)
class Member(relay.Node):
    id: relay.NodeID[str]
    email: str
    first_name: str
    last_name: str
    phone_number: str
    remote_id: UUID


@strawberry.input
class MemberRegisterInput:
    first_name: str
    last_name: str
    remote_id: UUID

    email: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def memberRegister(self, info, input: MemberRegisterInput) -> MutationResult:
        dto = MemberData(
            remote_id=input.remote_id,
            email=input.email,
            first_name=input.first_name,
            last_name=input.last_name,
            phone_number=input.phone_number,
        )

        result = await RegisterMemberService()(dto)

        return convert_service_result_to_mutation_result(result)


@strawberry.type
class Query:
    member: Member = relay.node()
    members: relay.ListConnection[Member] = strawberry.django.connection()
