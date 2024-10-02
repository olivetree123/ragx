FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN apt update && apt install -y gcc pkg-config default-libmysqlclient-dev && \
    pip install poetry && poetry config virtualenvs.create false && poetry install

COPY . .

RUN rm -rf /app/.venv

EXPOSE 5610

CMD [ "gunicorn", "-c", "gunicorn_config.py", "ragx.wsgi" ]