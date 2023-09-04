import django
from dependency_injector.wiring import inject, Provide
from django import db
from django.db import transaction
from microservice_utils.events import EventEnvelope


django.setup()
