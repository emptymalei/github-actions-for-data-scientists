FROM python:3.10-slim
MAINTAINER hi@leima.is

RUN apt-get update
RUN apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

ENV HOME="/root"
WORKDIR ${HOME}
RUN apt-get install -y git

ENV POETRY_VERSION=1.3.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"
RUN echo ‘export PATH="/root/.pyenv/bin:PATH"'>> /root/.bashrc &&\ echo 'eval "(pyenv init -)"’>> /root/.bashrc

ENV PYTHON_VERSION=3.10.9
RUN /bin/bash -c 'source $HOME/.bashrc; pyenv install ${PYTHON_VERSION}'
RUN /bin/bash -c 'source $HOME/.bashrc; pyenv global ${PYTHON_VERSION}'

WORKDIR /datascience

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install

EXPOSE 8888
CMD [ "poetry", "run" "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root" ]