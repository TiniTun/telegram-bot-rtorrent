#!/bin/sh

mkdir /downloads/.session
mkdir /downloads/watch
chown rtorrent:rtorrent /downloads/.session /downloads/watch

if [ -e /downloads/.session/rtorrent.lock ]; then
rm -f /downloads/.session/rtorrent.lock
fi

rm -f /etc/nginx/sites-enabled/*

cp /root/xmlrpc.nginx /etc/nginx/sites-enabled/

nginx -g "daemon off;"