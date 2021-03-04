from .resources.amount import Amount
from . import api

api.add_resource(Amount, '/request', '/request/<int:amount>', strict_slashes=False)
