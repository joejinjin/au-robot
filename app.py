import uvicorn
import hashlib
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse
import reply
import receive
from _chat import *


webapp = FastAPI()
weixin = 'joeandjin2017'


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
async def access(request: Request):
    data = (await request.body()).decode("utf-8")
    print("user => %s" % data)
    msg = receive.parse_xml(data)

    if isinstance(msg, receive.Msg) and msg.MsgType == 'text':
        to_user = msg.FromUserName
        from_user = msg.ToUserName

        print("content => %s" % msg.Content)

        messages = [{"role": "user", "content": msg.Content}]
        result = chat_completion(messages)

        reply_msg = reply.TextMsg(to_user, from_user, result)
        return reply_msg.send()

    return "success"


if __name__ == '__main__':
    # uvicorn.run(app=webapp, host="0.0.0.0", port=443, ssl_keyfile="key.pem", ssl_certfile="cert.pem", workers=1)
    uvicorn.run(app=webapp, host="0.0.0.0", port=80, workers=1)
