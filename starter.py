from flask import Flask, request, Response, jsonify, json
from markupsafe import escape

app = Flask(__name__)
enctype="multipart/form-data"

@app.route('/')
def index():
    return 'Index Page'

@app.route('/books')
def list_of_books():
    books = [
        {'name': 'The Call of the Wild', 'author': 'Jack London'},
        {'name': 'Heart of Darkness', 'author': 'Joseph Conrad'}
    ]
    #return json.dumps(books, indent=4)
    return jsonify(books)

if __name__ == "__main__":
    app.run(debug=True)
