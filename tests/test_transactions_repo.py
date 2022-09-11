import unittest
import mysql
from database.repo import TransactionsRepo

import mysql.connector

from utils import get_config

db_config = get_config()


class TestTransactionsRepo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cnx = mysql.connector.connect(
            host=db_config["TEST_MYSQL_HOST"],
            user=db_config["TEST_MYSQL_USER"],
            password=db_config["TEST_MYSQL_PASSWORD"],
            database=db_config["TEST_MYSQL_DB"],
            port=db_config["TEST_MYSQL_PORT"]
        )
        cursor = cnx.cursor(dictionary=True)

        query_1 = "DROP TABLE Transactions"
        try:
            cursor.execute(query_1)
            cnx.commit()
        except Exception as e:
            print(e)

        cursor = cnx.cursor(dictionary=True)

        query_2 = """CREATE TABLE Transactions (
                  id INTEGER NOT NULL PRIMARY KEY ,
                  amount FLOAT,
                  transaction_type VARCHAR(30) NOT NULL,
                  parent_id INTEGER
                )"""
        try:
            cursor.execute(query_2)
            cnx.commit()
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")

    def test_insert_transactions(self):
        self.transaction = TransactionsRepo(host=db_config["TEST_MYSQL_HOST"],
                                            user_name=db_config["TEST_MYSQL_USER"],
                                            password=db_config["TEST_MYSQL_PASSWORD"],
                                            db_name=db_config["TEST_MYSQL_DB"],
                                            port=db_config["TEST_MYSQL_PORT"])

        self.transaction.create_transaction(transaction_id=1, amount=100, parent_id=0, transaction_type="a")
        self.transaction.create_transaction(transaction_id=2, amount=200, parent_id=1, transaction_type="b")
        self.transaction.create_transaction(transaction_id=3, amount=300, parent_id=1, transaction_type="a")
        self.transaction.create_transaction(transaction_id=4, amount=400, parent_id=2, transaction_type="c")
        self.transaction.create_transaction(transaction_id=5, amount=500, parent_id=3, transaction_type="d")

        out_1 = self.transaction.get_transactions_by_type(transaction_type="a")

        self.assertEqual(len(out_1), 2)
        self.assertEqual([1, 3], [i[0] for i in out_1])

        self.transaction.create_transaction(transaction_id=6, amount=600, parent_id=5, transaction_type="e")
        self.transaction.create_transaction(transaction_id=7, amount=700, parent_id=6, transaction_type="a")





