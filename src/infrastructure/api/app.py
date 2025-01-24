import asyncio

from fastapi import FastAPI
import uvicorn

from src.infrastructure.api.routers.question_tree_api import router as qt_router

app = FastAPI()

app.include_router(qt_router, prefix="/api")


async def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    asyncio.run(main())
