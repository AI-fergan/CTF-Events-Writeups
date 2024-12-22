FROM python:3.12-slim-bookworm

ARG USERNAME=app
ARG PASSWORD=app
ARG GOTTY_VERSION=1.0.1

COPY entrypoint.sh /

COPY dictionary.txt wordle flag /opt/wordle/
COPY wordle.elf /opt/wordle/

RUN set -eux; \
    apt-get update; \
    apt-get install -y xxd curl; \
    \
    chmod +x /entrypoint.sh; \
    adduser --disabled-password --shell /bin/bash --gecos ${USERNAME} ${USERNAME}; \
    echo "${USERNAME}:${PASSWORD}" | chpasswd; \
    \
    curl -L https://github.com/yudai/gotty/releases/download/v${GOTTY_VERSION}/gotty_linux_$(dpkg --print-architecture).tar.gz \
      -o gotty.tar.gz; \
    tar -xzf gotty.tar.gz -C /usr/local/bin/; \
    rm -f gotty.tar.gz; \
    chmod +x /usr/local/bin/gotty

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends vim nano procps; \
    \
    pip install --no-cache-dir --upgrade pwntools ipython cron-descriptor; \
    \
    chmod 4555 /opt/wordle; \
    chmod 4555 /opt/wordle/wordle.elf; \
    chmod 0444 /opt/wordle/dictionary.txt; \
    chmod 0400 /opt/wordle/flag; \
    chmod +x /opt/wordle/wordle; \
    ln -s /opt/wordle /home/${USERNAME}/wordle

EXPOSE 3000
USER $USERNAME
ENV HOME=/home/${USERNAME}
ENV TERM=xterm-256color
WORKDIR /home/${USERNAME}
CMD [ "/entrypoint.sh" ]
