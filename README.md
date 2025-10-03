fastapi-async-chat/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ db.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ auth.py
│  ├─ crud.py
│  ├─ websocket_manager.py
│  └─ utils.py
├─ requirements.txt
└─ README.md


## Run command
```bash
  uv run fastapi dev --reload
```
## For production run command
```bash
  uv run fastapi run --reload
```


How to create alembic
```bash
  alembic init migrations
```
Configure Alembic
Edit alembic.ini and set the DB URL
```bash
    sqlalchemy.url = sqlite+aiosqlite:///./chat.db
    # sqlalchemy.url = postgresql+asyncpg://user:pass@localhost:5432/chatdb
```
Create migration:
```bash
    alembic revision --autogenerate -m "Initial migration"
```
Apply migration:
```bash
    alembic upgrade head
```

Edit migrations/env.py like this:
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
import asyncio

from app.database.session import Base  # <-- our models Base
from app import models   # <-- import models so Alembic knows them

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode with async engine."""
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
```
