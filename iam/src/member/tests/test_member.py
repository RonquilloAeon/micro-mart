from django.test import TestCase
from faker import Faker
from strawberry.relay.utils import to_base64

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
        member_id = to_base64("Member", member.id)

        expected_result = {
            "memberRegister": {
                "entities": [{"id": member_id, "name": "Member", "data": {}}],
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
            variables={"id": member_id},
        )

        expected_result = {
            "member": {
                "id": member_id,
                "firstName": member.first_name,
                "lastName": member.last_name,
                "phoneNumber": member.phone_number,
                "remoteId": str(member.remote_id),
            }
        }

        self.assertEqual(result.data, expected_result)

    def test_query_members(self):
        member_data = []

        for _ in range(5):
            member_data.append(
                {
                    "email": self.faker.email(),
                    "firstName": self.faker.first_name(),
                    "lastName": self.faker.last_name(),
                    "phoneNumber": self.faker.phone_number(),
                    "remoteId": self.faker.uuid4(),
                }
            )

        # Register members
        for member in member_data:
            self.query(
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
                variables={"input": member},
            )

        # Query for members
        result = self.query(
            """
            query members($first: Int) {
                members(first: $first) {
                    edges {
                        node {
                            id
                            firstName
                            lastName
                        }
                    }
                }
            }
            """
        )

        expected_edges = []
        member_data.reverse()

        for member in member_data:
            member_id = Member.objects.get(remote_id=member["remoteId"]).id

            expected_edges.append(
                {
                    "node": {
                        "id": to_base64("Member", member_id),
                        "firstName": member["firstName"],
                        "lastName": member["lastName"],
                    }
                }
            )

        expected_result = {"members": {"edges": expected_edges}}

        self.assertEqual(result.data, expected_result)
