
# ML model train & predict

Serve a machine learning model using scikit-learn, FastAPI and Docker.

## install runtime environment

- create new virtual env

   ```shell
   pyenv virtualenv 3.11.0 ml-demo
   pyenv local ml-demo
   pyenv activate ml-demo
   ```

- install scikit-learn

   <https://scikit-learn.org/stable/install>

   ```shell
   pip install -U scikit-learn
   ```

- install FastAPI and ASGI web server

   <https://fastapi.tiangolo.com/>

   ```shell
   pip install fastapi
   # one of ASGI (Asynchronous Server Gateway Interface) 
   pip install "uvicorn"
   ```

## train model

```shell
# with sys.path in the file train.py
python ./app/models/ml/train.py

# or using .env file with environment variable PYTHONPATH
export $(cat .env); python ./app/models/ml/train.py
```

## create api

please refer to [entry](./app/main.py) and [routes](./app/routes/)

## run and test

```shell
# start site
uvicorn app.main:app --port 8000

# predict
curl -X POST "http://localhost:8000/v1/iris/predict" -H\
 "accept: application/json"\
 -H "Content-Type: application/json"\
 -d "{\"data\":[[4.8,3,1.4,0.3],[2,1,3.2,1.1]]}"\
| jq
```

also can test via swagger ui at <http://localhost:8000/docs>

## deploy to Docker

run FastAPI in Docker, https://fastapi.tiangolo.com/deployment/docker/

try to build base image from `python:3.11-alpine`, but haven't made it.

to chekc if scikit-learn package is installed successfully

```shell
docker run --rm ml-alpine python -c "import sklearn; sklearn.show_versions()"
```

to run in Docker

```shell
./docker-deploy.sh
```

## pack app (source distribution)

install build tool

````shell
pip install build
````

create and edit [`pyproject.toml`](./pyproject.toml) or [`setup.py`](./setup.py.bak).

pack

```shell
python -m build --sdist --outdir build
```

to use (working in development mode)

```shell
python -m pip install -e .
```

## appendix

### docker tips

```shell
docker ps -a -f status=exited
docker rm $(docker ps -a -f status=exited -q)
docker rm $(docker ps -a -f status=exited -f status=created -q)
```

## reference

- [machine-learning-alpine image](https://github.com/Docker-Hub-frolvlad/docker-alpine-python-machinelearning/blob/master/Dockerfile)
- [get docker image size](https://gist.github.com/MichaelSimons/fb588539dcefd9b5fdf45ba04c302db6)
- [fastapi manchine learning skeleton](https://github.com/eightBEC/fastapi-ml-skeleton)
- [](https://medium.com/analytics-vidhya/serve-a-machine-learning-model-using-sklearn-fastapi-and-docker-85aabf96729b)
- [](https://engineering.rappi.com/serve-your-first-model-with-scikit-learn-flask-docker-df95efbbd35e)
