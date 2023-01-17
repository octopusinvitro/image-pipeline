FROM osgeo/gdal:ubuntu-small-3.6.2

RUN apt update && \
    apt install -y python3-pip && \
    apt install imagemagick -y && \
    apt autoremove -y && \
    apt autoclean -y && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install pipenv

RUN useradd -m ubuntu
USER ubuntu
ENV HOME /home/ubuntu
ENV PATH $PATH:$HOME/.local/bin
RUN echo "alias ls='ls --color=auto --group-directories-first -v'" >> ~/.bashrc

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --chown=ubuntu ./Pipfile ./
RUN pipenv install --deploy && pipenv install --dev --system
COPY --chown=ubuntu . .
