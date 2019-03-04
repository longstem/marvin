FROM python:3.7-alpine

RUN apk add --update \
	bash \
    make \
  && rm -rf /var/cache/apk/*

ENV FLASK_APP marvin.py
ENV FLASK_CONFIG production

COPY ./requirements /requirements
RUN pip install -r /requirements/docker.txt

COPY . /marvin

RUN adduser -D -u 1000 marvin
RUN chown -R marvin /marvin

WORKDIR /marvin

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
