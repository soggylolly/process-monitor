from flask import Flask  # import flask class

app = Flask(__name__)  # create application object

@app.route("/")  # when someone visits site root...
def hello():  # ...run this function
    return "Hello from Flask"  # whatever is returned becomes the page

if __name__ == "__main__":  # only start server if run directly
    app.run(debug=True)  # debug=True: auto reload on save, show errors in browser