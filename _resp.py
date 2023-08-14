##

def get_resp(code: int, msg):
    return {
        'code': code,
        'msg': msg,
    }


def resp_ok(msg):
    return get_resp(
        0, msg
    )


def resp_err(msg):
    return get_resp(
        -1, msg
    )
