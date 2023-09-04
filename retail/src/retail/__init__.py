from . import settings
from .containers import Container

# Configure dependency injection
container = Container()
container.config.from_dict(settings.__dict__)
