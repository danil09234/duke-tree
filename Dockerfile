FROM python:3.12.4-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN rm ./requirements.txt

COPY src ./src

ARG db_user
ARG db_password
ARG db_name
ARG db_host
ARG db_port
ARG db_name

ENV db_user $db_user
ENV db_password $db_password
ENV db_name $db_name
ENV db_host $db_host
ENV db_port $db_port
ENV db_name $db_name

ENTRYPOINT ["python", "-u", "-m", "src.scripts.study_programmes_parser.cli"]
