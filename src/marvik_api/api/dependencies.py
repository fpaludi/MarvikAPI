from typing import Generator
from fastapi import Depends
from logger import get_logger
from sqlalchemy.orm import Session
from marvik_api.db.session import SessionLocal
from marvik_api.db.crud.crud_endpoint import CRUDEndpointFactory, CRUDEndpoint


logger = get_logger(__name__)


def get_db() -> Generator[Session, None, None]:
    logger.debug("start db session")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.debug("close db session")
        db.close()


def get_crud_endpoint() -> CRUDEndpoint:
    db: Session = next(get_db())
    return CRUDEndpointFactory(db)
