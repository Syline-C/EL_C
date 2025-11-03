FROM ubuntu:22.04
LABEL maintainer="Choi"
LABEL version="1.0.0"
LABEL description="FPGA Artificial Inteligence Linux Env"


ENV CONDA_PLUGINS_AUTO_ACCEPT_TOS=yes

ARG TZ
ENV TZ=${TZ:-UTC}

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
#RUN ln -snf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

WORKDIR /home/conda


RUN apt-get update 
RUN apt-get install -y wget \
		vim git zsh language-pack-en python3-pip x11-apps tmux dbus-x11 pkg-config tcl clang tcl-dev \
		libreadline-dev bison flex python3-gi gobject-introspection gir1.2-gtk-3.0 graphviz python3-opengl mesa-utils \
		libgl1-mesa-glx

RUN update-locale

EXPOSE 80

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b  \
    && rm -f Miniconda3-latest-Linux-x86_64.sh


ENTRYPOINT ["/home/card/init.sh"]

SHELL ["/bin/bash"]

