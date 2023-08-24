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
        meta = sa.MetaData()
        t = sa.Table(
            "x",
            meta,
            sa.Column("y", sa.Integer, server_default="5", primary_key=True),
            sa.Column("data", sa.String(10)),
            implicit_returning=False,
        )

        await conn.run_sync(meta.create_all)
        await conn.execute(t.insert(), dict(data="data"))
        result = await conn.execute(t.select())
        assert list(result) == [(5, "data")]

        await conn.run_sync(meta.drop_all)

    async with engine.begin() as conn:
        meta = sa.MetaData()
        t = sa.Table(
            "x",
            meta,
            sa.Column(
                "y", sa.String(10), server_default="key_one", primary_key=True
            ),
            sa.Column("data", sa.String(10)),
        )

        await conn.run_sync(meta.create_all)
        await conn.execute(t.insert(), dict(data="data"))
        result = await conn.execute(t.select())
        assert list(result) == [("key_one", "data")]

        await conn.run_sync(meta.drop_all)


p = ArgumentParser()
p.add_argument('-D', '--dsn')
args = vars(p.parse_args())

asyncio.run(async_main(**args))
