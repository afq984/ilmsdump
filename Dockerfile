FROM docker.io/alpine:edge

RUN apk add python3 py3-pip py3-gunicorn \
    py3-aiohttp \
    py3-yarl \
    py3-lxml \
    py3-click \
    py3-wcwidth \
    py3-pillow \
    py3-jinja2

COPY . /build/
WORKDIR /build
RUN pip install --no-cache /build

ENV ADDR :8080
WORKDIR /

CMD exec gunicorn 'ilmsserve:make_app("/data")' --worker-class aiohttp.GunicornWebWorker --access-logfile - --bind $ADDR
