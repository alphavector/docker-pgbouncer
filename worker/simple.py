"""
Usage:
docker exec -it worker python -m simple -D postgresql+asyncpg://test:test@pgbouncer_ps:5432/test
docker exec -it worker python -m simple -D postgresql+asyncpg://test:test@pgbouncer_regular:5432/test
"""

import asyncio
from argparse import ArgumentParser

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine


async def async_main(dsn):
    engine = create_async_engine(
        dsn,
        echo=True,
        poolclass=sa.NullPool
    )

    async with engine.begin() as conn:
        await conn.execute(sa.select(1))


p = ArgumentParser()
p.add_argument('-D', '--dsn')
args = vars(p.parse_args())

asyncio.run(async_main(**args))
