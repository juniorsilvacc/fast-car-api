from fastapi import FastAPI
from fast_car_api.routers import router as car_router

app = FastAPI(
    title='Fast Car API',
    description='Modern Car API',
    version='0.1.0'
)

app.include_router(car_router)

@app.get('/test')
def read_root():
    return {'status': 'ok'}