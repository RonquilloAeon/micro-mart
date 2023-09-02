from django.test import TestCase
from faker import Faker

from core.testing import DependencyOverrideMixin, GraphQlMixin
from member.models import Member


class TestMemberSchema(TestCase, DependencyOverrideMixin, GraphQlMixin):
    def setUp(self):
        self.faker = Faker()

    def test_register_and_query(self):
        # Register a member
        result = self.query(
            """
            mutation ($input: MemberRegisterInput!) {
                memberRegister(input: $input) {
                    entities {
                        id
                        name
                        data
                    }
                    errors {
                        message
                    }
                    success
                }
            }
            """,
            variables={
                "input": {
                    "email": self.faker.email(),
                    "firstName": self.faker.first_name(),
                    "lastName": self.faker.last_name(),
                    "phoneNumber": self.faker.phone_number(),
                    "remoteId": self.faker.uuid4(),
                }
            },
        )

        member = Member.objects.last()

        expected_result = {
            "memberRegister": {
                "entities": [{"id": member.id, "name": "Member", "data": {}}],
                "errors": [],
                "success": True,
            }
        }

        self.assertEqual(result.data, expected_result)

        # Query for the member
        result = self.query(
            """
            query ($id: GlobalID!) {
                member(id: $id) {
                    id
                    firstName
                    lastName
                    phoneNumber
                    remoteId
                }
            }
            """,
            variables={"id": member.id},
        )

        expected_result = {
            "member": {
                "id": member.id,
                "firstName": member.first_name,
                "lastName": member.last_name,
                "phoneNumber": member.phone_number,
                "remoteId": member.remote_id,
            }
        }

        self.assertEqual(result.data, expected_result)
