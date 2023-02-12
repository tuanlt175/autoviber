FROM ubuntu:18.04

# Install basic packages and miscellaneous dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget \
    curl \
    git \
    redis-server \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
RUN apt update -y

# Create env
RUN conda clean --all --yes
RUN conda create -n viber python=3.7
RUN echo "source activate viber" > ~/.bashrc

# create folder in container
RUN mkdir /viber_bot \
    && mkdir /viber_bot/viber_bot

# run
COPY requirements.txt /viber_bot/requirements.txt
RUN /bin/bash -c  "source activate viber && \
    cd /viber_bot && \
    pip install -r requirements.txt"

COPY setup.py /viber_bot/setup.py
COPY viber_bot /viber_bot/viber_bot
COPY start_app.sh /viber_bot/start_app.sh

WORKDIR /viber_bot
RUN /bin/bash -c  "source activate viber && \
    python setup.py build_ext --inplace && \
    pip install -e ."

RUN chmod +x /viber_bot/start_app.sh

CMD ./start_app.sh

