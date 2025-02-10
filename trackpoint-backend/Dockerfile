FROM python:3.11.9-alpine3.20

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENV DOCKER=true
ENV TZ=Asia/Shanghai
EXPOSE 8000

CMD ["python","main.py"]