# image base python
FROM python:3.12-alpine3.20

LABEL authors="mpique"

RUN mkdir -p /input

# work directory in the container
WORKDIR /app

# copy at the app
COPY ./src /app/src
COPY ./tests /app/tests
COPY ./requirements.txt /app

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY ./pytest.ini /app


ENV PYTHONPATH=/app

# script python
CMD ["pytest", "-v"]

