FROM python:3.10-alpine as base

RUN apk update && apk upgrade

FROM base as builder

RUN apk add --no-cache build-base 

RUN python -m pip install --no-cache-dir -U pip wheel

COPY ./requirements.txt /service/

RUN python -OO -m pip wheel --no-cache-dir --wheel-dir=/root/wheels -r /service/requirements.txt

FROM base

COPY --from=builder /root/wheels /root/wheels

RUN python -m pip install --no-cache --no-index /root/wheels/* \ 
 && rm -rf /root/wheels

COPY . /service

RUN apk add --no-cache tzdata \
 && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
 && echo Asia/Shanghai > /etc/timezone \
 && apk del tzdata

WORKDIR /service

CMD [ "python", "main.py" ]
