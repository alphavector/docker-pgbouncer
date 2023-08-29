"""
Usage:
docker exec -it worker python -m old_oid -D postgresql+asyncpg://test:test@pgbouncer_ps:5432/test
docker exec -it worker python -m old_oid -D postgresql+asyncpg://test:test@pgbouncer_regular:5432/test
docker exec -it worker python -m old_oid -D postgresql+asyncpg://test:test@db:5432/test
"""

import asyncio
import enum

from argparse import ArgumentParser

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine
import sqlalchemy.dialects.postgresql as pg


async def async_main(dsn):
    engine = create_async_engine(
        dsn,
        echo=True,
        poolclass=sa.NullPool
    )

    class MyEnum(enum.Enum):
        foo = 1
        bar = 2

    async with engine.begin() as conn:
        meta = sa.MetaData()
        t = sa.Table(
            "foo",
            meta,
            sa.Column("bar", pg.ENUM(MyEnum)),
        )
        await conn.run_sync(meta.create_all)

        await conn.execute(t.insert(), {"bar": MyEnum.bar})
        await conn.rollback()

    async with engine.begin() as conn:
        meta = sa.MetaData()
        t = sa.Table(
            "foo",
            meta,
            sa.Column("bar", pg.ENUM(MyEnum)),
        )

        await conn.run_sync(meta.create_all)
        await conn.execute(t.insert(), {"bar": MyEnum.foo})

        await conn.run_sync(meta.drop_all)


p = ArgumentParser()
p.add_argument('-D', '--dsn')
args = vars(p.parse_args())

asyncio.run(async_main(**args))
