from urllib import request
from flask import Flask
from database.models.Transactions import Transactions


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"


@app.route("/transactionservice/transaction/:transactionid", methods=['POST'])
def sample():
    if request.method == "POST":
        transaction_id = request.form.get("transaction_id")
        amount = request.form.get("amount")
        transaction_type = request.form.get("transaction_type")
        parent_id = request.form.get("parent_id")

    return "blah"


@app.route("/transactionservice/types/$type")
def handle_get_transactions_for_type():
    return "Transactions type"

@app.route("/transactionservice/transaction/$transaction_id")
def create_transactions():
    return "created transactions"

@app.route("/transactionservice/sum/$transaction_id")
def handle_get_all_transactions_for_id():
    return "Handle all transaction for an id"


if __name__ == "main":
    app.run(debug=True, host="127.0.0.0")

