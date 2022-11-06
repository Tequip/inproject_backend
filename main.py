from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes.api import router
from app.core.celery_app import audit
from datetime import datetime
import pickle
import uvicorn


app = FastAPI(title=settings.APP_TITLE)
app.include_router(router, prefix=settings.API_V1_STR)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def audit_middle(request: Request, call_next):
    if settings.AUDIT:
        audit.delay(pickle.dumps({"method": request.method,
                                  "url": request.url,
                                  "headers": request.headers,
                                  "datetime": datetime.utcnow()}))
    return await call_next(request)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
