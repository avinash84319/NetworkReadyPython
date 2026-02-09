# Useing redis
FROM python:3.11.10-bullseye
 
# update all the repos
RUN apt-get update -q &&\
    apt-get upgrade -q -y

RUN pip install poetry

COPY pyproject.toml .

RUN poetry install

COPY . .

EXPOSE 5000

CMD ["poetry","run","python","servernode.py"]



