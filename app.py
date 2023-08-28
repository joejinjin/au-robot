import uvicorn
import hashlib
from fastapi import FastAPI, Request, BackgroundTasks, Response
from fastapi.responses import PlainTextResponse

import reply
import receive
from chat import *
from resp import *

webapp = FastAPI()
weixin = 'joeandjin2017'
user_cache = {}


@webapp.get("/token")
def token(request: Request):
    arr = [weixin, str(request.query_params["timestamp"]), str(request.query_params["nonce"])]
    arr.sort()

    tmp = ''.join(arr)
    enc = hashlib.sha1(tmp.encode("utf-8")).hexdigest()

    if enc == request.query_params["signature"]:
        return PlainTextResponse(request.query_params["echostr"])

    return PlainTextResponse('')


@webapp.post("/token")
async def access(request: Request, background: BackgroundTasks):
    media_type = "application/xml"

    data = (await request.body()).decode("utf-8")
    print("user => %s" % data)
    msg = receive.parse_xml(data)

    if isinstance(msg, receive.Msg) and msg.MsgType == 'text':
        to_user = msg.FromUserName
        from_user = msg.ToUserName

        if msg.FromUserName not in user_cache:
            background.add_task(running_question, msg.FromUserName, msg.Content.decode("utf-8"))
            text_msg = reply.TextMsg(to_user, from_user, "5秒后提醒我回复～")
            return Response(content=text_msg.send(), media_type=media_type)

        if user_cache[msg.FromUserName] == "0":
            text_msg = reply.TextMsg(to_user, from_user, "再等等不着急～")
            return Response(content=text_msg.send(), media_type=media_type)

        result = user_cache.pop(msg.FromUserName)
        text_msg = reply.TextMsg(to_user, from_user, result)
        return Response(content=text_msg.send(), media_type=media_type)

    return "success"


def running_question(user: str, content: str):
    user_cache[user] = "0"

    messages = [{"role": "user", "content": content}]
    result = chat_completion(messages)
    print("result => %s" % result)

    user_cache[user] = result


@webapp.post("/chat")
async def chat(request: Request):
    form = await request.json()

    system = form["system"]
    if not system: return resp_err('not good')
    user = form["user"]
    if not user: return resp_err('not good at all')

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    result = chat_completion(messages)
    return resp_ok(result)


if __name__ == '__main__':
    uvicorn.run(app=webapp, host="0.0.0.0", port=8080, workers=1)
