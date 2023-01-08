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

@app.route("/guildStats") #method = ["GET"]
def give_all_aviable_guild_stats():

    return()

@app.route("/raids") #method = ["GET"]
def create_new_raid ():

    return()

@app.route("/characters") #method = ["GET"]
def a():

    return()

@app.route("/raidRun", method = ["POST"])
def a():

    return()

@app.route("/raid/:id") #method = ["GET"]
def a():

    return()

@app.route("/raidRun/:id", method = ["GET", "PUT"])
def a():

    return()

@app.route("/raidRuns") #method = ["GET"]
def a():

    return()

if __name__ == "__main__":
    app.run(debug=True)
