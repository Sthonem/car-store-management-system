FROM python:3.13-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy

COPY . /app/

EXPOSE 4567

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]