FROM python:alpine

RUN pip install ping3 requests

RUN mkdir /code/
WORKDIR /code

CMD [ "python", "./pingmonitor.py", "run" ]
