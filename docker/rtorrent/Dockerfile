FROM ubuntu
USER root

# add ffmpeg ppa
ADD ./ffmpeg-next.list /etc/apt/sources.list.d/ffmpeg-next.list

# install
RUN apt-get update && \
    apt-get install -y --force-yes unzip unrar-free mediainfo curl nginx wget ffmpeg supervisor subversion gcc make checkinstall git automake && \
    rm -rf /var/lib/apt/lists/*

# Installs xmlrpc and libtorrent and rtorrent
#RUN apt-get -y update && apt-get -y install libxmlrpc-core-c3 libxmlrpc-core-c3-dev
#RUN apt-get purge rtorrent libtorrent*
WORKDIR /root/svn
RUN svn co https://xmlrpc-c.svn.sourceforge.net/svnroot/xmlrpc-c/advanced/ xmlrpc-c
WORKDIR /root/svn/xmlrpc-c
RUN ./configure --disable-cplusplus && \
    make && \
    checkinstall -D
WORKDIR /root/svn
RUN git clone https://github.com/rakshasa/libtorrent
WORKDIR /root/svn/libtorrent
RUN ./autogen.sh && \
    ./configure && \
    make && \
    checkinstall -D
WORKDIR /root/svn
RUN git clone https://github.com/rakshasa/rtorrent
WORKDIR /root/svn/rtorrent
RUN ./autogen.sh && \
    ./configure --with-xmlrpc-c && \
    make && \
    checkinstall -D
RUN echo "include /usr/local/lib" | tee -a /etc/ld.so.conf && \
    ldconfig

# configure nginx
ADD xmlrpc.nginx /root/

# configure rtorrent
RUN useradd -d /home/rtorrent -m -s /bin/bash rtorrent
ADD .rtorrent.rc /home/rtorrent/
RUN chown -R rtorrent:rtorrent /home/rtorrent

# add startup script
ADD startup.sh /root/

# configure supervisor
ADD supervisord.conf /etc/supervisor/conf.d/

EXPOSE 80
EXPOSE 49160
EXPOSE 49161

CMD ["supervisord"]