import time

from abc import abstractmethod, ABCMeta
from botocore.exceptions import ClientError
from typing import Dict, List, Any

from common.logger import logger
from common.dynamo.dynamo_connection import dynamodb
from common.utils import serialize_dynamo_item, deserialize_dynamo_item


class DynamoAbstractRepository(metaclass=ABCMeta):
    def _init_(self) -> None:
        self._logger = logger
        self._table = dynamodb.Table(self.table_name)

    @staticmethod
    def _serialize(item: Dict[str, Any]) -> Dict[str, Any]:
        return serialize_dynamo_item(item)

    @staticmethod
    def _deserialize(item: Dict[str, Any]) -> Dict[str, Any]:
        return deserialize_dynamo_item(item)

    @property
    @abstractmethod
    def table_name(self) -> str:
        pass  # pragma: no cover

    def scan_all(self) -> List[Dict[str, Any]]:
        items = []
        response = self._table.scan()

        for item in response["Items"]:
            deserialized_item = self._deserialize(item)
            items.append(deserialized_item)

        return items

    def get_item(self, key: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self._table.get_item(Key=key)
            return self._deserialize(response["Item"])
        except KeyError:
            message = (
                f"Item com chave {key} não encontrado na tabela {self.table_name}."
            )
            self._logger.error(message)

            raise KeyError(message)
        except Exception as error:  # pragma: no cover
            message = (
                f"Falha desconhecido ao consultar tabela {self.table_name}: {error}."
            )
            self._logger.error(message)

            raise Exception(message)

    def put_item(self, item: Dict[str, Any]) -> None:
        try:
            item = self._serialize(item)
            self._table.put_item(Item=item)
        except ClientError as client_error:  # pragma: no cover
            error_message = f"Falha ao tentar criar item na tabela {self.table_name}: {client_error.args}"
            self._logger.error(error_message)

            raise Exception(error_message)

    def batch_put(self, items: List[Dict[str, Any]]) -> None:
        self._logger.debug(
            f"Iniciando a criação de {len(items)} itens, em batch, "
            f"na tabela {self.table_name}. Itens duplicados serão ignorados..."
        )
        key_schema = self._table.key_schema
        keys = [attribute["AttributeName"] for attribute in key_schema]

        serialize_start = time.time()
        items = list(map(self._serialize, items))
        serialize_end = round(time.time() - serialize_start, 2)

        batch_start = time.time()
        try:
            with self._table.batch_writer(overwrite_by_pkeys=keys) as batch:
                for item in items:
                    batch.put_item(Item=item)
        except ClientError as client_error:  # pragma: no cover
            error_message = (
                f"Falha ao tentar criar items, em batch, na tabela "
                f"{self.table_name}: {client_error.args}"
            )
            self._logger.error(error_message)

            raise Exception(error_message)
        batch_end = round(time.time() - batch_start, 2)

        self._logger.info(
            f"Tempo das operações em batch para {len(items)} itens (segundos): "
            f"Serialização: {serialize_end} | Inserção: {batch_end}"
        )

    def update_item(
            self, key: Dict[str, Any], attributes: Dict[str, Any]
    ) -> Dict[str, Any]:  # pragma: no cover
        update_expression = "SET "
        expression_values = {}
        expression_names = {}

        attributes = self._serialize(attributes)

        for attribute_name, attribute_values in attributes.items():
            update_expression += f"#{attribute_name} = :{attribute_name}, "
            expression_values[f":{attribute_name}"] = attribute_values
            expression_names[f"#{attribute_name}"] = attribute_name
        update_expression = update_expression[:-2]

        try:
            response = self._table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ReturnValues="ALL_NEW",
            )
            return self._deserialize(response["Attributes"])
        except ClientError as client_error:
            message = f"Falha ao tentar atualizar item na tabela {self.table_name}: {client_error}"
            self._logger.error(message)

            raise Exception(message)

    def delete(self, key: Dict[str, Any]) -> None:  # pragma: no cover
        try:
            self._table.delete_item(Key=key)
        except ClientError as client_error:
            message = f"Falha ao tentar deletar item na tabela {self.table_name}: {client_error}"
            self._logger.error(message)

            raise Exception(message)

    def batch_delete(self, keys: List[Dict[str, Any]]) -> None:
        self._logger.debug(
            f"Iniciando a remoção de {len(keys)} itens, em batch, "
            f"na tabela {self.table_name}."
        )

        try:
            with self._table.batch_writer() as batch:
                for key in keys:
                    batch.delete_item(Key=key)
        except ClientError as client_error:  # pragma: no cover
            error_message = (
                f"Falha ao tentar remover items, em batch, na tabela "
                f"{self.table_name}: {client_error.args}"
            )
            self._logger.error(error_message)

            raise Exception(error_message)
