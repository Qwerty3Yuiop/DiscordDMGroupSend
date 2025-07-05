import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from api.task_handlers import router as task_handlers_router
from api.user_handlers import router as user_handlers_router

load_dotenv(".env")
app = FastAPI()

app.include_router(task_handlers_router)
app.include_router(user_handlers_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)