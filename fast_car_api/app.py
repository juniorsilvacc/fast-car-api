from fastapi import FastAPI

app = FastAPI(
    title='Fast Car API',
    description='Modern Car API',
    version='0.1.0'
)

@app.get('/carros')
def read_root():
    return {'status': 'ok'}