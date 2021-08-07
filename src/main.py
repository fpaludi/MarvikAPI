import uvicorn
from fastapi import FastAPI
from settings import settings  # noqa
from logger import configure_logger
from marvik_api.api.api import api_router

app = FastAPI(title="MarvikAPI")
app.include_router(api_router)

configure_logger()


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=80)
