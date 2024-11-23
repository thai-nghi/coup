from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src import db_tables, schemas


async def all_countries(db_session: AsyncSession) -> list[schemas.Country]:
    query = select(db_tables.countries)

    rows = await db_session.execute(query)

    return [
        schemas.Country(label=row._mapping["label"], value=row._mapping["id"])
        for row in rows
    ]


async def fetch_data_of_field(
    db_session: AsyncSession, field: schemas.MetadataFields
) -> list[schemas.Country]:
    if field == schemas.MetadataFields.COUNTRY:
        return await all_countries(db_session)
