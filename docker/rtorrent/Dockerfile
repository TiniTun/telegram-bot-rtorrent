FROM ubuntu:14.04
USER root

# add ffmpeg ppa
#ADD ./ffmpeg-next.list /etc/apt/sources.list.d/ffmpeg-next.list + apt-get install ffmpeg

# install
RUN apt-get update && \
    apt-get install -y --force-yes unzip unrar-free mediainfo curl nginx wget supervisor subversion gcc make \
    checkinstall git automake libtool libcppunit-dev zlib1g-dev libssl-dev build-essential autoconf libncurses5-dev \
    libncursesw5-dev libcurl4-openssl-dev openssl libsigc++-2.0-dev && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/rtorrent -m -s /bin/bash rtorrent

# Installs xmlrpc and libtorrent and rtorrent
#RUN apt-get -y update && apt-get -y install libxmlrpc-core-c3 libxmlrpc-core-c3-dev
#RUN apt-get purge rtorrent libtorrent*
WORKDIR /root/svn
RUN svn co https://xmlrpc-c.svn.sourceforge.net/svnroot/xmlrpc-c/advanced/ xmlrpc-c
WORKDIR /root/svn/xmlrpc-c
RUN ./configure --disable-cplusplus && \
    make && \
    make install
WORKDIR /root/svn
#RUN git clone https://github.com/rakshasa/libtorrent
RUN wget https://github.com/rakshasa/libtorrent/archive/0.13.4.tar.gz -O libtorrent.tar.gz
RUN tar xvf libtorrent.tar.gz
WORKDIR /root/svn/libtorrent-0.13.4
RUN ./autogen.sh && \
    ./configure && \
    make && \
    make install
WORKDIR /root/svn
#RUN git clone https://github.com/rakshasa/rtorrent
RUN wget http://rtorrent.net/downloads/rtorrent-0.9.4.tar.gz -O rtorrent.tar.gz
RUN tar xvf rtorrent.tar.gz
RUN apt-get update && \
    apt-get install -y --force-yes libsigc++-2.0-0c2a libcurl3-dev && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /root/svn/rtorrent-0.9.4
RUN ./autogen.sh && \
    ./configure --with-xmlrpc-c && \
    make && \
    make install
RUN echo "include /usr/local/lib" | tee -a /etc/ld.so.conf && \
    ldconfig

WORKDIR /root
RUN rm -rf svn
# configure nginx
ADD xmlrpc.nginx /root/

# configure rtorrent
#RUN useradd -d /home/rtorrent -m -s /bin/bash rtorrent
ADD .rtorrent.rc /home/rtorrent/
RUN chown -R rtorrent:rtorrent /home/rtorrent

# add startup script
ADD startup.sh /root/
RUN chmod +x /root/startup.sh

# configure supervisor
ADD supervisord.conf /etc/supervisor/conf.d/

EXPOSE 80
EXPOSE 49160
EXPOSE 49161

CMD ["supervisord"]