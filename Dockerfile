FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt install -y gcc pkg-config default-libmysqlclient-dev

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY . .

EXPOSE 5610

CMD [ "gunicorn", "-c", "gunicorn_config.py", "ragx.wsgi" ]