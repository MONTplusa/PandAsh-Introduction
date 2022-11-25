from app.app import app
from waitress import serve


@app.route("/home", methods=["GET"])
def home():
    return "ホームページ（仮）"


if __name__ == "__main__":

    serve(app, host="0.0.0.0", port=5000)
