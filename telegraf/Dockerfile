FROM telegraf:alpine

LABEL version="1.0"
LABEL description="Telegraf docker image with custom setup"

WORKDIR /app
USER root

ADD telegraf.template.conf telegraf.template.conf

ADD run.sh run.sh
RUN chmod +x /app/*.sh

CMD ["/bin/sh", "/app/run.sh"]
