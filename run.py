from app.models import student
from app.api import *
from app.app import app
from waitress import serve
import flask
import requests
import contextlib
import time
from math import floor
import sqlalchemy.exc
from app.settings import session


@app.route("/home", methods=["GET"])
def home():
    return "ホームページ（仮）"


@app.route("/update", methods=["GET"])
def update():
    ses = requests.Session()
    user = get_user_json(ses)
    item = get_user_info_from_api(user)
    new_data = [item]
    with open_db_ses() as db_ses:
        # 既に同じidのものがないか確認し、あれば中止、なければ追加
        student_data = (
            db_ses.query(student.Student)
            .filter(student.Student.student_id == item["student_id"])
            .all()
        )
        if len(student_data) > 0:
            old_name = student_data[0].fullname
            db_ses.bulk_update_mappings(student.Student, new_data)
            return f"名前を更新しました。{old_name}->{item['fullname']}"
        db_ses.execute(student.Student.__table__.insert(), new_data)
    return f"登録しました。ID:{item['student_id']}, 名前:{item['fullname']}"


@app.route("/register", methods=["GET"])
def register():
    # id,nameをパラメータとして受け取る
    new_data = []
    item = {}
    item["student_id"] = flask.request.args.get("id")
    if item["student_id"] == None:
        return "idパラメータがありません"
    item["fullname"] = flask.request.args.get("name")
    if item["fullname"] == None:
        return "nameパラメータがありません"

    new_data.append(item)
    with open_db_ses() as db_ses:
        # 既に同じidのものがないか確認し、あれば中止、なければ追加
        student_data = (
            db_ses.query(student.Student)
            .filter(student.Student.student_id == item["student_id"])
            .all()
        )
        if len(student_data) > 0:
            old_name = student_data[0].fullname
            db_ses.bulk_update_mappings(student.Student, new_data)
            return f"名前を更新しました。{old_name}->{item['fullname']}"
        db_ses.execute(student.Student.__table__.insert(), new_data)
        # 追加データが少数の場合は以下のほうが自然かも
        # new_item = student.Student()
        # new_item.student_id = flask.request.args.get("id")
        # new_item.fullname = flask.request.args.get("name")
        # db_ses.add(new_item)
    return f"登録しました。ID:{item['student_id']}, 名前:{item['fullname']}"


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


@app.before_request
def before_request():
    if flask.request.endpoint == "is_even":
        flask.abort(403)
    if flask.request.endpoint == "is_even_2":
        flask.abort(403)


@app.errorhandler(403)
def forbidden(error):
    message = "アクセスが拒否されました。"
    return message, 403


@app.errorhandler(404)
def page_not_found(error):
    message = "お探しのページは見つかりませんでした。"
    return message, 404


@contextlib.contextmanager
def open_db_ses():
    db_ses = session()
    try:
        yield db_ses
        db_ses.commit()
    except sqlalchemy.exc.SQLAlchemyError:
        db_ses.rollback()
        raise
    finally:
        db_ses.close()


if __name__ == "__main__":

    serve(app, host="0.0.0.0", port=5000)
