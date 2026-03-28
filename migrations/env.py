import asyncio
from logging.config import fileConfig
import os

from geoalchemy2 import Geography, Geometry, Raster
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.config import settings
from app.core.models.base import Base

config = context.config

fileConfig(
    os.path.join(os.getcwd(), "logging.conf"),
    disable_existing_loggers=False
)

target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", str(settings.db.url))


def include_object(object, name, type_, reflected, compare_to, parent_names=None):
    # Получаем схему
    schema = getattr(object, 'schema', None) or \
             getattr(getattr(object, 'table', None), 'schema', None)
    
    # Фильтруем системные схемы
    if schema in ("topology", "tiger", "tiger_data"):
        return False
    
    # Для таблиц: проверяем есть ли в наших моделях
    if type_ == "table":
        return name in target_metadata.tables
    
    # Для индексов/колонок: проверяем таблицу-родителя
    table_name = None
    if hasattr(object, 'table'):
        table_name = object.table.name
    elif parent_names and 'table_name' in parent_names:
        table_name = parent_names['table_name']
    
    # Если таблица не наша — пропускаем
    if table_name and table_name not in target_metadata.tables:
        return False
    
    # Фильтруем spatial индексы
    if type_ == "index":
        try:
            col = object.expressions[0]
            if isinstance(col.type, (Geometry, Geography, Raster)):
                return False
        except (AttributeError, IndexError):
            pass
    
    return True


def render_item(obj_type, obj, autogen_context):
    if obj_type == 'type' and isinstance(obj, (Geometry, Geography, Raster)):
        import_name = obj.__class__.__name__
        autogen_context.imports.add(f"from geoalchemy2 import {import_name}")
        return "%r" % obj
    return False


async def ensure_database_exists_async():
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(settings.db.admin_url, isolation_level="AUTOCOMMIT", future=True)
    db_name = settings.db.url.rsplit("/", maxsplit=1)[-1]

    async with engine.begin() as conn:
        result = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": db_name},
        )
        exists = result.scalar()
        if not exists:
            await conn.execute(text(f'CREATE DATABASE "{db_name}"'))

    await engine.dispose()


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        render_item=render_item,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
        render_item=render_item,
    )  

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(ensure_database_exists_async())
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()