import uvicorn
import hashlib
from fastapi import FastAPI, Request, BackgroundTasks
# from _chat import *
# from _resp import *

webapp = FastAPI()
weixin = 'joeandjin2017'


@webapp.get("/token")
def token(request: Request):
    arr = [weixin, str(request.query_params["timestamp"]), str(request.query_params["nonce"])]
    arr.sort()

    tmp = ''.join(arr)
    enc = hashlib.sha1(tmp.encode("utf-8")).hexdigest()

    if enc == request.query_params["signature"]:
        return request.query_params["echostr"]

    return None


# @webapp.post("/chat")
# async def chat(request: Request, background: BackgroundTasks):
#     request_body = await request.json()
#     question = request_body["question"]
#
#     messages = [{"role": "user", "content": question}]
#     result = chat_completion(messages)
#
#     return resp_ok(result)


if __name__ == '__main__':
    # uvicorn.run(app=webapp, host="0.0.0.0", port=443, ssl_keyfile="key.pem", ssl_certfile="cert.pem", workers=1)
    uvicorn.run(app=webapp, host="0.0.0.0", port=80, workers=1)
