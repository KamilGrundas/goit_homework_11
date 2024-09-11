FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install .

ENTRYPOINT [ "python","/usr/local/lib/python3.11/site-packages/application_personal_assistant/main.py" ]