
from fastapi.encoders import jsonable_encoder

from starlette.requests import Request
from starlette.responses import JSONResponse
from uvicorn import run
from Exception_handling.classes import InvalidUserException, InvalidDataException, UserNotFound

from models import ErrorModel
from fastapi import FastAPI

from routes.localization import translate_message
from routes.routes import app


main = FastAPI()
@main.exception_handler(UserNotFound)
async def user_not_found(request: Request, exc: UserNotFound):
    language = request.headers.get("Accept-Language", "en")
    response = ErrorModel(status_code=exc.status, detail=translate_message(("User {} not found").format(exc.username), language), message="There is no such user")
    return JSONResponse(status_code=exc.status, content=response.dict())


@main.exception_handler(InvalidUserException)
async def invalid_user_handling(request: Request, exc: InvalidUserException):
    error = jsonable_encoder(ErrorModel(status_code=exc.status, detail=exc.detail, message=exc.message))
    return JSONResponse(status_code=exc.status, content=error, headers={"PORT-x": str(request.client.port)})

@main.exception_handler(InvalidDataException)
async def invalid_data_handling(request: Request, exc: InvalidDataException):
    error = jsonable_encoder(ErrorModel(status_code=exc.status, detail=exc.detail, message=exc.message))
    return JSONResponse(status_code=exc.status, content=error, headers={"PORT-x": str(request.client.port)})



main.include_router(app)

# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
# asyncio.run(init_models())

if __name__ == "__main__":
    run("main:main", host="localhost", port=8005, reload=True)

