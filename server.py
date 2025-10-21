from flask import Flask
import database as db

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

# Define sql queries
def createTable():
    db.runQuery(db.create_test_table)
def dropTable():
    db.runQuery(db.drop_test_table)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)