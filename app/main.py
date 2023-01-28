import uvicorn
from fastapi import FastAPI

import models
from database.database import engine
from routes import wells_api, materials_api, productions_api

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(wells_api.router)
app.include_router(materials_api.router)
app.include_router(productions_api.router)

if __name__ == '__main__':
    uvicorn.run(app)
