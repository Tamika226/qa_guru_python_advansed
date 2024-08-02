FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./reqres_fast_api /code/reqres_fast_api

CMD ["fastapi", "run", "reqres_fast_api/main.py", "--port", "80"]