import uvicorn

from app.config.setting_env import settings

if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=settings.port,
        loop="asyncio",
        workers=1
    )
