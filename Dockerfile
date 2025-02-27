# Container Build File for the webapp ( Flask - Granian )
# there is an issue in compiling orjson on python 3.13
FROM python:3.12

# WORKDIR /usr/src/app

COPY ./requirements.txt /requirements/

RUN pip3 install --no-cache-dir -r /requirements/requirements.txt

COPY ./src /app

# COPY ./containers/redis/tls /redis_tls

ENV PYTHONPATH=/app

WORKDIR /app/

RUN chmod +x /app/start_server.sh

# COPY ./ssl/fullchain.pem /ssl/fullchain.pem
# COPY ./ssl/privkey.pem /ssl/privkey.pem

# ENV GRANIAN_SSL_CERTIFICATE=/ssl/fullchain.pem
# ENV GRANIAN_SSL_KEYFILE=/ssl/privkey.pem

EXPOSE 80
EXPOSE 443

ENV TZ=Asia/Jerusalem
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ >/etc/timezone

CMD ["./start_server.sh"]
