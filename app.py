from flask import Flask, request, jsonify
from database.repo import TransactionsRepo
from utils import get_config

app = Flask(__name__)

_CONFIG = get_config()

_TRANSACTIONS_REPO = TransactionsRepo(
    host=_CONFIG['MYSQL_HOST'],
    user_name=_CONFIG['MYSQL_USER'],
    password=_CONFIG['MYSQL_PASSWORD'],
    port=int(_CONFIG['MYSQL_PORT']),
    db_name=_CONFIG['MYSQL_DB']
)


@app.route("/transactionservice/transaction/<int:transaction_id>", methods=['POST', 'GET'])
def sample(transaction_id):
    if request.method == "POST":
        amount = request.json.get("amount")
        transaction_type = request.json.get("transaction_type")
        parent_id = request.json.get("parent_id")
        print(amount, request, transaction_type)
        if None in [transaction_id, amount, transaction_type]:
            return jsonify({"err": "Mandatory params missing"}), 400
        
        try:
            _TRANSACTIONS_REPO.create_transaction(transaction_id=transaction_id,
                                                  amount=float(amount), transaction_type=transaction_type,
                                                  parent_id=int(parent_id))
            return jsonify({"msg": "success"}), 200
        except ValueError as ve:
            print(ve)
            return jsonify({"err": "Invalid parent id"}), 400
        except Exception as e:
            print(e)
            return jsonify({"err": "Something went wrong"}), 500
    elif request.method == "GET":
        try:
            transaction_data = _TRANSACTIONS_REPO.get_transactions_by_id(transaction_id)
            return jsonify({"transactions": transaction_data}), 200
        except Exception as e:
            print(e)
            return jsonify({"err": "Something went wrong"}), 500


@app.route("/transactionservice/types/<string:transaction_type>", methods=['GET'])
def handle_get_transactions_for_type(transaction_type):
    if request.method == "GET":
        try:
            data = _TRANSACTIONS_REPO.get_transactions_by_type(transaction_type=transaction_type)
            return jsonify({"transactions": data}), 200
        except Exception as e:
            print(e)
            return jsonify({"err": "Something went wrong"}), 500


@app.route("/transactionservice/sum/<int:transaction_id>", methods=['GET'])
def handle_get_all_transactions_for_id(transaction_id):
    if request.method == "GET":
        try:
            transaction_sum = _TRANSACTIONS_REPO.transactions_sum_from_parent_id(transaction_id)
            return jsonify({"sum": transaction_sum}), 200
        except Exception as e:
            print(e)
            return jsonify({"err": "Something went wrong"}), 500


if __name__ == "main":
    app.run()
