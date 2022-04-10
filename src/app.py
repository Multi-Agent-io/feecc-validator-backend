import typing as tp

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from _logging import CONSOLE_LOGGING_CONFIG
from database import MongoDbWrapper
from key_types import KeyTypes
from models import GenericResponse, UnitData

# apply logging configuration
logger.configure(handlers=[CONSOLE_LOGGING_CONFIG])

# create app
app = FastAPI(
    title="Feecc Validator backend",
    description="A validation service for Feecc end users",
)

# set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = None


@app.on_event("startup")
def startup_event() -> None:
    global DB
    DB = MongoDbWrapper()


@app.get("/api/v1/unit-data", response_model=tp.Union[UnitData, GenericResponse])  # type: ignore
async def get_unit_data(key_type: KeyTypes, key_value: str) -> tp.Union[UnitData, GenericResponse]:
    try:
        unit = await MongoDbWrapper().get_unit_by_key(key_type, key_value)
        return UnitData(
            status_code=status.HTTP_200_OK,
            detail="Requested unit retrieved",
            unit_data=unit,
        )

    except Exception as e:
        return GenericResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during unit retrieval: {e}",
        )


if __name__ == "__main__":
    uvicorn.run("app:app", port=8084)
