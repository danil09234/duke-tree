FROM python:3.12.4-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN rm ./requirements.txt

COPY src ./src

ENTRYPOINT ["python", "-u", "-m", "src.main"]
