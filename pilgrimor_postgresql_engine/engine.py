from typing import Any, List, Optional, Tuple

import psycopg


class PostgreSQLEngine:
    """
    Engine to execute sql quries.

    The engine works with the database.

    It performs sql queries, return data if needed
    and returns the necessary information
    for the migrator.

    By default, the request is executed in a transaction
    (in psycopg this is autocommit=False)
    but this behavior can be changed by
    adding autocommit=True.

    However, there is a nuance in this method,
    only one command will be executed not in a transaction,
    if there are several of them,
    then the rest will be in a transaction.
    """

    def __init__(self, database_url: str) -> None:
        """
        Creates connection pool.

        :param database_url: url to database.
        """
        self.database_url = database_url

    def execute_sql_with_return(
        self,
        sql_query: str,
        sql_query_params: Tuple[Any],
        in_transaction: Optional[bool] = True,
    ) -> Optional[List[Any]]:
        """
        Executes sql query and return output.

        By default query

        :param sql_query: sql query to execute.
        :param sql_query_params: parameters for sql query.
        :param in_transaction: execute in transaction or not.

        :return: None or list with results.
        """
        autocommit = False
        if not in_transaction:
            autocommit = True

        with psycopg.connect(self.database_url, autocommit=autocommit) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query=sql_query,
                    params=sql_query_params,
                )
                result = cursor.fetchall()

        return self._form_result(result=result)

    def execute_sql_no_return(
        self,
        sql_query: str,
        sql_query_params: Tuple[Any],
        in_transaction: Optional[bool] = True,
    ) -> None:
        """
        Executes sql query and do not return any output.

        :param sql_query: sql query to execute.
        :param sql_query_params: parameters for sql query.
        :param in_transaction: execute in transaction or not.
        """
        autocommit = False
        if not in_transaction:
            autocommit = True

        with psycopg.connect(self.database_url, autocommit=autocommit) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query=sql_query,
                    params=sql_query_params,
                )

    def _form_result(self, result: Any) -> Optional[List[Any]]:
        """
        Create list with record from query result.

        :param result: result from query.

        :returns: :return: None or list with results.
        """
        result_length = len(result)

        if result_length == 1:
            return list(result[0])
        elif result_length == 0:
            return None

        to_return_result = []
        for record in result:
            if len(record) == 1:
                to_return_result.append(record[0])
            elif len(record) > 1:
                to_return_result.append(record)
        return to_return_result
