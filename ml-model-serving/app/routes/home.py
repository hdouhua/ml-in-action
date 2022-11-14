from fastapi import APIRouter

app_home = APIRouter()


@app_home.get('/', tags=['Intro'])
async def info():
  return {"message": "hello world!"}


#comment testing
@app_home.get('/ver', tags=['Intro'])
async def ver():
  """get version"""
  return {"ver": "1.0.0"}


@app_home.get('/health')
async def health():
  """Return service health"""
  return 'ok'
