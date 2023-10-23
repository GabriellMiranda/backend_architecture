import os

from abc import abstractmethod, ABCMeta
from typing import Type
from psycopg2 import connect as connect_postgres
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AbstractConnection(metaclass=ABCMeta):
    def _init_(
            self,
            user_env_var: str,
            password_env_var: str,
            host_env_var: str,
            port_env_var: str,
            database_env_var: str,
            base_class: Type[DeclarativeMeta],
            connection_name: str,
            driver: str,
    ) -> None:
        self._user_env_var = user_env_var
        self._password_env_var = password_env_var
        self._host_env_var = host_env_var
        self._port_env_var = port_env_var
        self._database_env_var = database_env_var

        self._base_class = base_class
        self.__connection_name = connection_name
        self._driver = driver

    @property
    def connection_name(self) -> str:
        return self.__connection_name

    @property
    def driver(self) -> str:
        return self._driver

    @abstractmethod
    def get_connection(self):
        pass  # pragma: no cover

    @property
    def base_class(self) -> Type[DeclarativeMeta]:
        return self._base_class


class PostgresDBConnection(AbstractConnection):
    def _init_(self, user_env_var: str, password_env_var: str, host_env_var: str, port_env_var: str,
               database_env_var: str, base_class: Type[DeclarativeMeta], connection_name: str, **kwargs) -> None:
        super()._init_(
            user_env_var,
            password_env_var,
            host_env_var,
            port_env_var,
            database_env_var,
            base_class,
            connection_name,
            "postgresql+psycopg2://",
        )

    def get_connection(self):
        return connect_postgres(
            user=os.environ[self._user_env_var],
            password=os.environ[self._password_env_var],
            host=os.environ[self._host_env_var],
            port=os.environ[self._port_env_var],
            dbname=os.environ[self._database_env_var],
        )


class StagingConnection(PostgresDBConnection):
    def _init_(self, **kwargs) -> None:
        super()._init_("STAGING_USER", "STAGING_PASSWORD", "STAGING_HOST", "STAGING_PORT", "STAGING_DATABASE", Base,
                       "DATABASE")
