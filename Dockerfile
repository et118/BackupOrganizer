FROM python:3.13-alpine3.21 as base

ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN mkdir src 

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src ./src

EXPOSE 5000

#--------DEVELOPMENT---------

FROM base as dev
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt


#The sourcecode will be linked with a bindmount in docker-compose
CMD ["flask", "--app", "./src/restinterface.py", "run", "--host=0.0.0.0"]
#-------PRODUCTION-------------

FROM base as prod

RUN pip install gunicorn

WORKDIR ./src
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "restinterface:app"]

#----------TESTING---------

FROM dev as test

COPY ./tests /app/tests
COPY ./pytest.ini /app/

CMD ["pytest"]
