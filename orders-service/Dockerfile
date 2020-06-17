FROM python:3.8-alpine

LABEL Name=items_service Version=0.0.1
EXPOSE 8000

WORKDIR /app
ADD . /app

RUN apk update && apk add postgresql-dev gcc musl-dev
RUN apk add build-base

# Using pip:
RUN python -m pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]