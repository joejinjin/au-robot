import uvicorn
import hashlib
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse
import reply
import receive
from _chat import *


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
    data = (await request.body()).decode("utf-8")
    print("user => %s" % data)
    msg = receive.parse_xml(data)

    if isinstance(msg, receive.Msg) and msg.MsgType == 'text':
        to_user = msg.FromUserName
        from_user = msg.ToUserName

        if msg.FromUserName in user_cache:
            if user_cache[msg.FromUserName] == "0":
                reply_msg = reply.TextMsg(to_user, from_user, "再等等，不着急～")
                return reply_msg.send()

            reply_msg = reply.TextMsg(to_user, from_user, user_cache.pop(msg.FromUserName))
            return reply_msg.send()

        print("content => %s" % msg.Content.decode("utf-8"))
        background.add_task(running_question, msg.FromUserName, msg.Content.decode("utf-8"))

        reply_msg = reply.TextMsg(to_user, from_user, "给我点时间哈，5秒之后提醒我回复～")
        return reply_msg.send()

    return "success"


def running_question(user: str, content: str):
    user_cache[user] = "0"
    messages = [{"role": "user", "content": content}]
    result = chat_completion(messages)
    user_cache[user] = result


if __name__ == '__main__':
    # uvicorn.run(app=webapp, host="0.0.0.0", port=443, ssl_keyfile="key.pem", ssl_certfile="cert.pem", workers=1)
    uvicorn.run(app=webapp, host="0.0.0.0", port=80, workers=1)
