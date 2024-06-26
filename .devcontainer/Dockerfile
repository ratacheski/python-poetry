FROM debian:bookworm-slim as builder
WORKDIR /opt

ENV PYENV_ROOT="/opt/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        libbz2-dev \
        libffi-dev \
        liblzma-dev \
        libncurses5-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        make \
        zlib1g-dev

SHELL [ "/bin/bash", "-o", "pipefail", "-c" ]
RUN curl https://pyenv.run | bash

COPY ./.python-version ./pyproject.toml ./poetry* /opt/
RUN pyenv install "$(cat .python-version)" && \
    pyenv global "$(cat .python-version)"

# hadolint ignore=DL3013
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install && \
    rm -rf ~/.cache

FROM mcr.microsoft.com/devcontainers/base:bookworm
COPY --from=builder /opt/.pyenv /opt/.pyenv

ENV PYENV_ROOT="/opt/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
ENV PYTHONUNBUFFERED True

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends graphviz\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R vscode $PYENV_ROOT
