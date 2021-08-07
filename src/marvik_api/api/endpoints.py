from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from logger import get_logger
from marvik_api.api.dependencies import get_crud_endpoint
from marvik_api.db.crud.crud_endpoint import CRUDEndpoint
from marvik_api.schemas.endpoint import UpdateEndpoint, EndpointCounters
from marvik_api.schemas.timestamp import TimestampMode, TimestampResponse


router = APIRouter()
logger = get_logger(__name__)

DataNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Data not found",
)


@router.get("/counters", response_model=EndpointCounters)
def get_endpoint_counter(crud_endpoint: CRUDEndpoint = Depends(get_crud_endpoint),):
    logger.info(f"GET '/counters' endpoint")
    get_endpoint = crud_endpoint.get_by_name(name="get")
    updated_get = None
    if get_endpoint:
        update_get_endpoint = UpdateEndpoint(count=get_endpoint.count + 1)
        updated_get = crud_endpoint.update(
            db_obj=get_endpoint, obj_in=update_get_endpoint
        )

    post_endpoint = crud_endpoint.get_by_name(name="post")

    if updated_get and post_endpoint:
        return EndpointCounters(
            get_counter=updated_get.count, post_counter=post_endpoint.count
        )
    else:
        raise DataNotFoundException


@router.post("/timestamp", response_model=TimestampResponse)
def timestamp(
    timestamp_mode: TimestampMode,
    crud_endpoint: CRUDEndpoint = Depends(get_crud_endpoint),
):
    logger.info(f"POST '/timestamp' endpoint")
    post_endpoint = crud_endpoint.get_by_name(name="post")
    if post_endpoint:
        update_post_endpoint = UpdateEndpoint(count=post_endpoint.count + 1)
        crud_endpoint.update(db_obj=post_endpoint, obj_in=update_post_endpoint)
    else:
        raise DataNotFoundException

    date = datetime.now()
    if timestamp_mode.mode:
        result = TimestampResponse(timestamp=date.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        result = TimestampResponse(timestamp=date.strftime("%Y-%d-%m"))

    return result
