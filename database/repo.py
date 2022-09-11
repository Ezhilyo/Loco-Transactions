from asyncio.log import logger
import mysql.connector


class TransactionsRepo:
    def __init__(self, host: str, db_name: str, user_name: str, password: str):
        self._mysql_db = mysql.connector.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name
        )
        self._cursor = self._mysql_db.cursor()
    
    def _is_cyclic(self, transaction_id: int, parent_id: int):
        query = f"""
            with recursive cte as (
            select * from Transactions where id={transaction_id}
            union
            select T.id, T.amount, T.parent_id from Transactions T join cte C on C.id=T.parent_id
            )
            select * from cte where T.id = {parent_id};
        """
        try:
            # checking if parent id is already a child of transaction id. to prevent cyclicity
            data = self._cursor.execute(query)
            return len(data) == 0
        except Exception as e:
            logger.exception(f"Error occurred while fetching child transanction data for transaction_id: {transaction_id} due to {e}")
            raise Exception("Some error occured")

    def create_transaction(self, transaction_id: int, amount: float, transaction_type: str, parent_id: int):
        if self._is_cyclic(transaction_id=transaction_id, parent_id=parent_id):
            raise ValueError("Invalid parentId provided")
        query = f"INSERT INTO Transactions(id, amount, transaction_type, parent_id) values({transaction_id, amount, transaction_type, parent_id})"
        try:
            self._cursor.execute(query)
            self._mysql_db.commit()
        except Exception as e:
            logger.exception(f"Exception occurred while inserting into db for transaction_id: {transaction_id}")
            raise Exception("Error occurred while inserting into db")
    
    def update_transaction(self, transaction_id: int, amount: float, transaction_type: str, parent_id: int):
        if self._is_cyclic(transaction_id=transaction_id, parent_id=parent_id):
            raise ValueError("Invalid parentId provided")
        query = f"UPDATE Transactions set amount={amount}, transaction_type={transaction_type}, parent_id={parent_id}) where id={transaction_id}"
        try:
            self._cursor.execute(query)
            self._mysql_db.commit()
        except Exception as e:
            logger.exception(f"Error occurred while inserting into db for transaction_id: {transaction_id} due to {e}")
            raise Exception("Error occurred while inserting into db")
    
    def get_transactions_by_type(self, transaction_type: str):
        query = "SELECT transaction_id, amount, transaction_type, parent_id from Transactions where transaction_type={transaction_type}"
        try:
            self._cursor.execute(query)
            return self._cursor.fetchall()
        except Exception as e:
            logger.exception(f"Error occurred while fetching data for transaction_type: {transaction_type} due to {e}")
            raise Exception("Error occurred")

    def get_transactions_by_id(self, transaction_id: int):
        query = "SELECT transaction_id, amount, transaction_type, parent_id from Transactions where id={transaction_id}"
        try:
            self._cursor.execute(query)
            self._cursor.fetchall()
        except Exception as e:
            logger.exception(f"Error occurred while fetching data for transaction_id: {transaction_id} due to {e}")
            raise Exception("Error occurred")
    
    def transactions_sum_from_parent_id(self, transaction_id: int):
        query = f"""
            with recursive cte as (
            select * from Transactions where id={transaction_id}
            union
            select T.id, T.amount, T.parent_id from Transactions T join cte C on C.id=T.parent_id
            )
            select sum(amount) as t_sum from cte;
        """

        try:
            self._cursor.execute(query)
            return self._cursor.fetchone().get('t_sum', 0)
        except Exception as e:
            logger.exception(f"Error occurred while fetching data for transaction_id: {transaction_id} due to {e}")
            raise Exception("Error occurred")
