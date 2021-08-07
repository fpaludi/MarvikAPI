from typing import Any, List
from dependency_injector.providers import Factory
from marvik_api.db.crud.crud_base import CRUDBase
from marvik_api.db.models.endpoint import Endpoint as EndpointDBModel
from marvik_api.schemas.endpoint import Endpoint, CreateEndpoint, UpdateEndpoint


class CRUDEndpoint(CRUDBase[EndpointDBModel, Endpoint, CreateEndpoint, UpdateEndpoint]):
    pass


CRUDEndpointFactory = Factory(CRUDEndpoint, model=EndpointDBModel, schema=Endpoint)
