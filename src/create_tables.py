import contextlib
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from marvik_api.db.base_class import Base
from marvik_api.db.models.endpoint import Endpoint


def create_tables(engine: Engine, session: Session):  # noqa
    print(f"\nCreating Tables in {engine.url}\n")
    Base.metadata.create_all(engine)
    endpoint = Endpoint(name="get", count=0,)
    session.add(endpoint)
    endpoint = Endpoint(name="post", count=0,)
    session.add(endpoint)
    try:
        session.commit()
    except IntegrityError:
        print("Row already exist")


def delete_tables(engine: Engine, session: Session):  # noqa
    print("\nRemoving Tables...\n")
    session.close_all()
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(f"TRUNCATE TABLE public.{table.name} RESTART IDENTITY CASCADE;")
        trans.commit()
    print("\nTables removed")


if __name__ == "__main__":
    from settings import settings  # noqa
    from marvik_api.db.session import engine, SessionLocal

    session = SessionLocal()
    # delete_tables(engine, session)
    create_tables(engine, session)
    session.close()  # noqa
    engine.dispose()
