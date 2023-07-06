import fastapi
import uvicorn
from fastapi import responses
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routers import auth, chat, conversation, health, test, upload
from core.config import chatbot, settings
from core.env_var import *

app = fastapi.FastAPI(
    title=settings.APP_NAME,
    version=settings.releaseId,
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    chatbot.initialize()

app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(
    conversation.router, prefix=settings.API_V1_STR, tags=["conversation"]
)
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["health"])
app.include_router(upload.router, prefix=settings.API_V1_STR, tags=["upload"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["chat"])
app.include_router(test.router, prefix=settings.API_V1_STR, tags=["test"])


@app.get("/", include_in_schema=False)
async def index() -> responses.RedirectResponse:
    return responses.RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8185,
        reload=True,
    )
