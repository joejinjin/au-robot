import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks
from _chat import *
from _resp import *

webapp = FastAPI()


@webapp.post("/chat")
async def chat(request: Request, background: BackgroundTasks):
    request_body = await request.json()
    question = request_body["question"]

    messages = [{"role": "user", "content": question}]
    result = chat_completion(messages)

    return resp_ok(result)


if __name__ == '__main__':
    uvicorn.run(app=webapp, host="0.0.0.0", port=443, ssl_keyfile="key.pem", ssl_certfile="cert.pem", workers=1)
