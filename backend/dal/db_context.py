from sqlalchemy import create_engine, event, inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from typing import Generic, TypeVar
from sqlalchemy import update as sql_update, delete as sql_delete
from sqlalchemy.future import select
from config import SQLALCHEMY_DATABASE_URL
from fastapi.concurrency import run_in_threadpool
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from uuid import uuid4
import json

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
import abc


class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


T = TypeVar("T")
IGNORE_TABLES = [
    "access_log",
    "activity_log",
    "activity_detail",
    "client_token",
    "error_log",
    "signature",
    "media",
    "manifest_chat",
    "tasks",
    "manifest_transportation_travels",
]


class SessionWrapper:
    def __init__(self, session):
        self.session = session

    def __getattr__(self, name):
        return getattr(self.session, name)

    # def add(self, instance):
    #     self.session.add(instance)
    #     self.session.sync_session.flush()

    def withTitle(self, title, description=""):
        self.info["action_title"] = title
        self.info["description"] = description
        return self

    def withSignature(self, signature_id="", reason=""):
        self.info["signature_id"] = signature_id
        self.info["reason"] = reason
        return self

    def withReason(self, reason):
        self.info["reason"] = reason
        return self

    def withDescription(self, description):
        self.info["description"] = description
        return self

    def withActionType(self, actionType):
        self.info["action_type"] = actionType
        return self

    def withModule(self, module):
        self.info["module"] = module
        return self

    def add_ignore_table(self, table_name):
        self.info["ignored_tables"].append(table_name)
        return self

    def with_manifest_info(self, manifest_id, status, order_no):
        self.info["manifest_id"] = manifest_id
        self.info["status"] = status
        self.info["order_no"] = order_no
        return self

    def add_ignore_column(self, table_name, column_name):
        ignore_table = f"{table_name}.{column_name}"
        self.info["ignored_tables"].append(ignore_table)
        return self


class AsyncDatabaseSession(metaclass=Singleton):
    def __init__(self) -> None:
        self.session = None
        self.engine = None
        self.init()
        print("****** Init AsyncDatabaseSession")

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self):
        self.engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL, future=True, echo=True, pool_pre_ping=True
        )

        self.session = sessionmaker(
            self.engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
        )

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def commit_rollback(self):
        try:
            await self.commit()
        except Exception:
            await self.rollback()
            raise
        finally:
            await self.close()

    @staticmethod
    def is_ignore_table(session, obj):
        if obj.__tablename__ in IGNORE_TABLES:
            return True

        if obj.__tablename__ in session.info.get("ignored_tables", []):
            return True
        return False

    @staticmethod
    def is_ignore_column(session, obj, attr):
        if attr.key in session.info.get("ignored_columns", []):
            return True
        return False

    @staticmethod
    def get_primary_key(obj):
        primary_keys = inspect(obj).mapper.primary_key
        primary_key_info = [
            {"column": key.key, "value": getattr(obj, key.key)} for key in primary_keys
        ]
        primary_key_name = ",".join([info["column"] for info in primary_key_info])
        primary_key_value = ",".join([str(info["value"]) for info in primary_key_info])
        return primary_key_name, primary_key_value

    @staticmethod
    def before_commit(session):
        changes = []
        session.info["transaction_id"] = str(uuid4())
        for obj in session.dirty:
            if AsyncDatabaseSession.is_ignore_table(session, obj):
                continue

            change = {}
            table_name = obj.__tablename__
            event_type = "1"
            primary_key_name, primary_key_value = AsyncDatabaseSession.get_primary_key(
                obj
            )
            count_new = 0
            for attr in inspect(obj).attrs:
                if AsyncDatabaseSession.is_ignore_column(session, obj, attr):
                    continue
                if attr.history.has_changes():
                    if attr.key == "is_deleted" and attr.value == True:
                        event_type = "2"

                    change[attr.key] = {
                        "o": (
                            attr.history.deleted[0] if attr.history.deleted else None
                        ),
                        "n": attr.value,
                    }
                    count_new += 1
                else:
                    change[attr.key] = {"o": attr.value}
            if change and count_new > 0:
                now = datetime.utcnow()
                changes.append(
                    {
                        "table": table_name,
                        "event": event_type,
                        "primary_key_name": primary_key_name,
                        "primary_key_value": primary_key_value,
                        "data": change,
                        "created_at": now,
                    }
                )

        for obj in session.new:

            # if obj.__tablename__ == "signature":
            #     for attr in inspect(obj).attrs:
            #         if attr.key == "signature_id":
            #             session.info["signature_id"] = attr.value
            #         if attr.key == "reason":
            #             session.info["reason"] = attr.value

            if AsyncDatabaseSession.is_ignore_table(session, obj):
                continue

            change = {}
            table_name = obj.__tablename__
            event_type = "0"
            primary_key_name, primary_key_value = AsyncDatabaseSession.get_primary_key(
                obj
            )
            for attr in inspect(obj).attrs:
                if AsyncDatabaseSession.is_ignore_column(session, obj, attr):
                    continue
                change[attr.key] = {
                    "n": attr.value,
                }

            if change:
                now = datetime.utcnow()
                changes.append(
                    {
                        "table": table_name,
                        "event": event_type,
                        "primary_key_name": primary_key_name,
                        "primary_key_value": primary_key_value,
                        "data": change,
                        "created_at": now,
                    }
                )

        for obj in session.deleted:
            if AsyncDatabaseSession.is_ignore_table(session, obj):
                continue
            change = {}
            table_name = obj.__tablename__
            primary_key_name, primary_key_value = AsyncDatabaseSession.get_primary_key(
                obj
            )
            event_type = "2"
            for attr in inspect(obj).attrs:
                if AsyncDatabaseSession.is_ignore_column(session, obj, attr):
                    continue
                change[attr.key] = {"o": attr.value}

            if change:
                now = datetime.utcnow()
                changes.append(
                    {
                        "table": table_name,
                        "event": event_type,
                        "primary_key_name": primary_key_name,
                        "primary_key_value": primary_key_value,
                        "data": change,
                        "created_at": now,
                    }
                )
        if len(changes) > 0:
            pass
            # AsyncDatabaseSession.save_audit_log(session, changes)
            # session.info["changes"] = changes

    @staticmethod
    def after_commit(session):
        session.info["ignored_tables"] = []
        session.info["ignored_columns"] = []
        session.info["transaction_id"] = ""
        session.info["manifest_id"] = ""
        session.info["status"] = ""
        session.info["order_no"] = ""
        session.info["module"] = ""
        session.info["action_title"] = ""
        session.info["description"] = ""
        session.info["reason"] = ""
        session.info["action_type"] = ""
        session.info["signature_id"] = ""
        # changes = session.info.pop("changes", [])
        # data = json.dumps(changes, default=str)
        # print(data)

    @asynccontextmanager
    async def get_session(
        self, isCommit: bool = False, currentSession: AsyncSession = None
    ):
        # currentSession = user_context.db_session.get()
        if currentSession is None:
            async with self.session() as ss:
                try:
                    event.listen(ss.sync_session, "before_commit", self.before_commit)
                    event.listen(ss.sync_session, "after_commit", self.after_commit)
                    currentSession = SessionWrapper(ss)
                    # user_context.db_session.set(currentSession)
                    yield currentSession
                    if isCommit:
                        ss.commit()

                except Exception as ex:
                    await currentSession.rollback()
                    raise ex
                finally:
                    try:
                        await currentSession.close()
                    except Exception as ex:
                        pass
        else:
            yield currentSession


dbContext = AsyncDatabaseSession


class BaseRepository:
    model = Generic[T]

    @classmethod
    async def create(cls, **kwargs):
        ctxdb = dbContext()
        async with ctxdb.get_session() as ctx:
            model = cls.model(**kwargs)
            ctx.add(model)
            await ctx.commit()
            return model

    @classmethod
    async def get_all(cls):
        ctxdb = dbContext()
        async with ctxdb.get_session() as ctx:
            query = select(cls.model)
            return (await ctx.execute(query)).scalars().all()

    @classmethod
    async def get_by_id(cls, model_id: str):
        ctxdb = dbContext()
        async with ctxdb.get_session() as ctx:
            query = select(cls.model).where(cls.model.id == model_id)
            return (await ctx.execute(query)).scalar_one_or_none()
