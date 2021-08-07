from pydantic import BaseModel, Field


class Endpoint(BaseModel):
    # id: int
    name: str
    count: int = Field(default=0)

    class Config:
        orm_mode = True


class UpdateEndpoint(BaseModel):
    count: int


class CreateEndpoint(Endpoint):
    pass


class EndpointCounters(BaseModel):
    get_counter: int
    post_counter: int
