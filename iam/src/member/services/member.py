import typing
from dataclasses import dataclass
from uuid import UUID

from asgiref.sync import sync_to_async
from django.db import transaction, utils
from django.db.models import Q

from core.services import ServiceResult, execute_safely
from member.models import Member


@dataclass
class MemberData:
    remote_id: UUID
    first_name: str
    last_name: str
    email: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None


class RegisterMemberService:
    @execute_safely
    async def __call__(self, data: MemberData) -> Member:
        result = ServiceResult()

        try:
            member = await sync_to_async(self._register_member)(data)
            result.add_entity(member)
        except (RuntimeError, utils.IntegrityError):
            result.add_error(
                "Member was not added. The member conflicts with an already-registered member."
            )

        return result

    @transaction.atomic
    def _register_member(self, data: MemberData) -> Member:
        existing_member = Member.objects.filter(
            Q(email=data.email) | Q(phone_number=data.phone_number)
        )

        if existing_member:
            raise RuntimeError("Member already exists")

        member = Member.objects.register(
            remote_id=data.remote_id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone_number=data.phone_number,
        )
        return member
