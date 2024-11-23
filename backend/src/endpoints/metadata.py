from typing import Any

from fastapi import APIRouter
from src import schemas
from src.dependencies import DatabaseDependency
from src.services import metadata

router = APIRouter(prefix="/metadata", tags=["metadata"])


@router.post("/")
async def get_metadata(
    db_session: DatabaseDependency, request_fields: list[schemas.MetadataFields]
) -> dict[str, Any]:
    result = {}
    for field in request_fields:
        result[field.value] = await metadata.fetch_data_of_field(db_session, field)

    return result
