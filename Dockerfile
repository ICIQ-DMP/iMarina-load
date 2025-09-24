
# image base python
FROM python:3.12-alpine3.20

LABEL authors="mpique"

# work directory in the container
WORKDIR /app

# copy requirements
COPY requirements.txt .

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

# script python for main
CMD ["python", "main.py"]
