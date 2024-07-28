from fastapi import FastAPI
from fastapi_pagination import add_pagination
from routers import status, users
import uvicorn
import logging
import users_load

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')
    uvicorn.run(app)
    logger.info('Finished')
