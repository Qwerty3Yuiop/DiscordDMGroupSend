from dotenv import load_dotenv 
from api.handlers import router
load_dotenv(".env")

if __name__ == '__main__':
    import uvicorn
    # For development, you can run directly:
    uvicorn.run(router, host="0.0.0.0", port=8000)