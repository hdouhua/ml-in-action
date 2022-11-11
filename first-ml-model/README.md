
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

- install FastAPI

   <https://fastapi.tiangolo.com/>

   ```shell
   pip install fastapi
   # one of ASGI (Asynchronous Server Gateway Interface) 
   pip install "uvicorn[standard]"
   ```

## train model

```shell
cd models
python ml/train.py
```

## create api

TBD

## run and test

```shell
# start site
uvicorn main:app --port 8000

# predict
curl -X POST "http://127.0.0.1:8000/v1/iris/predict" -H\
 "accept: application/json"\
 -H "Content-Type: application/json"\
 -d "{\"data\":[[4.8,3,1.4,0.3],[2,1,3.2,1.1]]}"\
| jq
```

can open swagger ui at <http://127.0.0.1:8000/docs>

## deploy in Docker

run FastAPI in Docker, https://fastapi.tiangolo.com/deployment/docker/

try to build base image from `python:3.11-alpine`, but haven't done yet.

to chekc if scikit-learn package is installed successfully

```shell
docker run --rm ml-alpine python -c "import sklearn; sklearn.show_versions()"
```

## appendix

### install python env

install pyenv

```shell
pip install pyenv
```

after installed add PATH to `.bashrc` or `.zshrc`

```shell
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# init pyenv automatically
#eval "$(pyenv virtualenv-init -)"
```

list all supported pytnon above 3.1x in pyenv

```shell
pyenv install --list | grep " 3\.1\d"
pyenv install -v 3.11.0
```

pyenv commands reference

```shell
pyenv commands
pyenv versions

# get where the python / pip is installed
pyenv which python
pyenv which pip

# create virtual python env
pyenv virtualenv <python_version> <environment_name>

pyenv local <environment_name>

pyenv activate <environment_name>
pyenv deactivate

# uninstall/delete virtualenv
pyenv uninstall <environment_name>
# or
pyenv virtualenv-delete <environment_name>
```

for more, please refer to <https://realpython.com/intro-to-pyenv>

### code format

- install yapf

   ```shell
   pip install yapf
   ```

- create and edit `.style.yapf` file, the setting is key=value pair

   please refer to [.style.yapf](./.style.yapf)

- run command

   ```shell
   # run code format recursively and write back to file
   yapf -i -r app/
   ```

### docker tips

```shell
docker ps -a -f status=exited
docker rm $(docker ps -a -f status=exited -q)
docker rm $(docker ps -a -f status=exited -f status=created -q)
```

## reference

- [machine-learning-alpine image](https://github.com/Docker-Hub-frolvlad/docker-alpine-python-machinelearning/blob/master/Dockerfile)
- [get docker image size](https://gist.github.com/MichaelSimons/fb588539dcefd9b5fdf45ba04c302db6)
- [](https://medium.com/analytics-vidhya/serve-a-machine-learning-model-using-sklearn-fastapi-and-docker-85aabf96729b)
- [](https://engineering.rappi.com/serve-your-first-model-with-scikit-learn-flask-docker-df95efbbd35e)
