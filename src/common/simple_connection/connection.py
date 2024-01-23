from abc import abstractmethod, ABCMeta
from typing import Dict

from psycopg2 import connect as connect_postgres
from pymysql import connect as connect_mysql

from common.logger import logger
from common.aws.secret_manager import SecretManager


class AbstractConnection(metaclass=ABCMeta):
    def _init_(self, secret_name: str) -> None:
        self.__secrets_manager = SecretManager()
        self._logger = logger

        self._db_host: str = ""
        self._db_port: str = ""
        self._db_user: str = ""
        self._db_password: str = ""
        self._db_name: str = ""
        self.__set_credentials(secret_name)

    def __set_credentials(self, secret_name: str) -> None:
        """
        Conexão em ambiente local utiliza um túnel, logo os valores recuperados do secret manager
        não servirão, o memso vale para ambiente de testes que aponta para banco local em docker.
        """
        self._logger.debug(
            f"Obtendo credenciais do banco a partir do Secret {secret_name}"
        )
        secret_value: Dict[str, str]

        if len(secret_name.split(",")) == 1:  # pragma: no cover
            secret_value = self.__secrets_manager.get_secret_value(secret_name)
        else:
            secret_name = secret_name.split(",")
            secret_value = {
                "host": secret_name[0],
                "port": secret_name[1],
                "username": secret_name[2],
                "password": secret_name[3],
                "db_name": secret_name[4],
            }

        self._db_host = secret_value.get("proxy_host", secret_value["host"])
        self._db_port = int(secret_value["port"])
        self._db_user = secret_value["username"]
        self._db_password = secret_value["password"]
        self._db_name = secret_value["db_name"]

        self._logger.debug(
            f"Credenciais lidas do Secret {secret_name}: \n"
            f"DB_HOST: {self._db_host}\nDB_PORT: {self._db_port}\nDB_USER: {self._db_user}\n"
            f"DB_NAME: {self._db_name}"
        )

    @abstractmethod
    def get_connection(self):
        pass  # pragma: no cover


class PostgresConnection(AbstractConnection):
    def get_connection(self):
        return connect_postgres(
            user=self._db_user,
            password=self._db_password,
            host=self._db_host,
            port=self._db_port,
            dbname=self._db_name,
        )


class MysqlConnection(AbstractConnection):
    def get_connection(self):
        return connect_mysql(
            user=self._db_user,
            password=self._db_password,
            host=self._db_host,
            port=self._db_port,
            database=self._db_name,
        )