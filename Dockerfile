
# image base python
FROM python:3.12-alpine3.20

LABEL authors="mpique"

RUN mkdir -p /input

# work directory in the container
WORKDIR /app

# copy at the app
COPY ./src /app/src
COPY ./requirements.txt /app

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

# script python for main
CMD ["python", "/app/src/main.py", "--imarina-input", "/input/iMarina.xlsx", "--a3-input", "/input/A3.xlsx", "--countries-dict", "/input/countries.xlsx", "--jobs-dict", "/input/Job_Descriptions.xlsx"]
