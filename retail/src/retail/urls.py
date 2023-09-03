from django.urls import path
from strawberry.django.views import AsyncGraphQLView

from .graphql import schema

urlpatterns = [
    path("graphql", AsyncGraphQLView.as_view(schema=schema)),
]
