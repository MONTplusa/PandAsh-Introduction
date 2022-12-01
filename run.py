from app.app import app
from waitress import serve
import flask


@app.route("/home", methods=["GET"])
def home():
    return "ホームページ（仮）"


@app.route("/", methods=["GET"])
def root():
    # return flask.redirect("http://localhost:5000/home")でもOK
    return flask.redirect(flask.url_for("home"))  # この"home"は関数名


if __name__ == "__main__":

    serve(app, host="0.0.0.0", port=5000)
