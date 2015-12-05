#!/bin/sh

mkdir /downloads/.session
mkdir /downloads/watch
chown rtorrent:rtorrent /downloads/.session /downloads/watch

rm -f /downloads/.session/rtorrent.lock

rm -f /etc/nginx/sites-enabled/*

rm -rf /etc/nginx/ssl

# Basic auth enabled by default
site=xmlrpc.nginx

cp /root/$site /etc/nginx/sites-enabled/

nginx -g "daemon off;"