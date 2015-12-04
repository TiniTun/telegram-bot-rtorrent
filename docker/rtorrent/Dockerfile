FROM ubuntu
USER root

# add ffmpeg ppa
ADD ./ffmpeg-next.list /etc/apt/sources.list.d/ffmpeg-next.list

# install
RUN apt-get update && \
    apt-get install -y --force-yes rtorrent unzip unrar-free mediainfo curl wget ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Installs xmlrpc
RUN apt-get -y update && apt-get -y install libxmlrpc-core-c3 libxmlrpc-core-c3-dev

# configure rtorrent
RUN useradd -d /home/rtorrent -m -s /bin/bash rtorrent
ADD .rtorrent.rc /home/rtorrent/
RUN chown -R rtorrent:rtorrent /home/rtorrent

# Creates rtorrent Service
WORKDIR     /etc/service/rtorrent
ADD         ./run_rtorrent.sh /etc/service/rtorrent/run
RUN         chmod +x ./run

CMD ["/etc/service/rtorrent/run"]