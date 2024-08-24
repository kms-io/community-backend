from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Settings
from routes.user_route import router as user_router
from routes.auth_route import router as auth_router
settings = Settings()


app = FastAPI(
    title="헬스커뮤 API",
    description="헬스커뮤 API 서버입니다.",
    version="0.1.0",
    contact={
        "name": "MoonSu",
        "url": "https://github.com/sounmu",
        "email": "sukkang_@korea.ac.kr"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

origins = [
    "https://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "헬스커뮤 API 서버입니다."}