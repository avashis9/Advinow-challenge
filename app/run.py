import uvicorn
from fastapi import FastAPI # need python-multipart
from starlette.middleware.cors import CORSMiddleware

import views

app = FastAPI(title="AdviNow Interview Challenge", version="1.6")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(views.router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8013)
