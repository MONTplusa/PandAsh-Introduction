from app.app import app
from waitress import serve
import flask


@app.route("/home", methods=["GET"])
def home():
    return "ホームページ（仮）"


@app.route("/test/is_even/<num>", methods=["GET"])
def is_even(num):

    if int(num) % 2 == 0:
        return "even"
    return "odd"


@app.route("/test/is_even_2", methods=["GET"])
def is_even_2():
    num = flask.request.args.get("num")
    if num == None:
        return "error"
    if int(num) % 2 == 0:
        return "even"
    return "odd"


@app.route("/", methods=["GET"])
def root():
    # return flask.redirect("http://localhost:5000/home")でもOK
    return flask.redirect(flask.url_for("home"))  # この"home"は関数名


if __name__ == "__main__":

    serve(app, host="0.0.0.0", port=5000)
