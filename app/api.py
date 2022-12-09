import json


def get_user_info_from_api(user):
    fullname = user.get("displayName")
    student_id = user.get("id")
    return {"student_id": student_id, "fullname": fullname}


def get_user_json(ses):
    res = ses.get("https://panda.ecs.kyoto-u.ac.jp/direct/user/current.json")
    try:
        return res.json()
    except json.JSONDecodeError as e:
        return {}
