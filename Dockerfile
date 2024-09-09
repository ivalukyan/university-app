FROM python:3.12-alpine3.20

RUN mkdir /backend
WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install 

COPY . .

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]