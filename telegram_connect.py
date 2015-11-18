#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import time
import subprocess
import os
import urllib

from settings import Settings

requests.packages.urllib3.disable_warnings()

offset = 0


def check_updates():
    global offset
    data = {'offset': offset + 1, 'limit': 5, 'timeout': 0}  # Формируем параметры запроса
    request = requests_http('/getUpdates', data)

    if request:
        if not request.json()['ok']:
            return False
    else:
        return False

    for update in request.json()['result']:  # Проверка каждого элемента списка
        offset = update['update_id']  # Извлечение ID сообщения

        # Ниже, если в обновлении отсутствует блок 'message'
        # или же в блоке 'message' отсутствует блок 'text', тогда
        # if not 'message' in update or not 'text' in update['message']:
        mtype = type_message(update)
        if not mtype:
            log_event('Unknown update: %s' % update)  # сохраняем в лог пришедшее обновление
            continue  # и переходим к следующему обновлению

        from_id = update['message']['chat']['id']  # Извлечение ID чата (отправителя)
        name = update['message']['chat']['username']  # Извлечение username отправителя
        if from_id != Settings.adminId:  # Если отправитель не является администратором, то
            send_text("You're not autorized to use me!", from_id)  # ему отправляется соответствующее уведомление
            log_event('Unautorized: %s' % update)  # обновление записывается в лог
            continue  # и цикл переходит к следующему обновлению
        message = update['message'][mtype]  # Извлечение текста сообщения
        parameters = (offset, name, from_id, message)
        log_event('Message (id%s) from %s (id%s): "%s"' % parameters)  # Вывод в лог ID и текста сообщения

        # В зависимости от сообщения, выполняем необходимое действие
        run_command(*parameters)


def run_command(offset, name, from_id, cmd):
    if cmd == '/ping':  # Ответ на ping
        send_text(from_id, 'pong')  # Отправка ответа

    elif cmd == '/help':  # Ответ на help
        send_text(from_id, 'No help today. Sorry.')  # Ответ

    elif 'file_id' in cmd:
        request = requests_http('/getFile', {'file_id': cmd['file_id']})

        if not request.json()['ok']:
            return False

        file_mime = cmd['mime_type']
        if file_mime != 'application/x-bittorrent':
            send_text(from_id, "Mime type file\'s is not true")  # ему отправляется соответствующее уведомление
            return False
            # continue # и цикл переходит к следующему обновлению
        file_name = cmd['file_name']

        torrent_file = request.json()['result']
        file_path = torrent_file['file_path']

        tfile = urllib.urlopen(Settings.urlFile + Settings.token + '/' + file_path).read()

        dir_torrent_file = '/mount/flash/Torrent/file/'

        if not os.path.isdir(dir_torrent_file):
            send_text(from_id, "Dir torrent file is not dir")
            return False
        f = open(dir_torrent_file + file_name, "wb")
        f.write(tfile)
        f.close()

        # log_event(request.json()['result'])
        send_text(from_id, 'Ok!')  # Отправка ответа

    else:
        send_text(from_id, 'Got it.')  # Отправка ответа


def log_event(text):
    """
    Процедура логгирования
    ToDo: 1) Запись лога в файл
    """
    event = '%s >> %s' % (time.ctime(), text)
    print(event)


def send_text(chat_id, text):
    """Отправка текстового сообщения по chat_id
    ToDo: повторная отправка при неудаче"""
    log_event('Sending to %s: %s' % (chat_id, text))  # Запись события в лог
    data = {'chat_id': chat_id, 'text': text}  # Формирование запроса
    request = requests_http('/sendMessage', data)  # HTTP запрос
    if not request.status_code == 200:  # Проверка ответа сервера
        return False  # Возврат с неудачей
    return request.json()['ok']  # Проверка успешности обращения к API


def type_message(update):
    _type = False
    if 'message' in update:
        if 'text' in update['message']:
            _type = 'text'
        elif 'document' in update['message']:
            _type = 'document'

    if _type:
        return _type
    else:
        # log_event('Unknown update: %s' % update) # сохраняем в лог пришедшее обновление
        return False


def requests_http(method, data):
    try:
        request = requests.post(Settings.urlBot + Settings.token + method, data=data)
    except:
        log_event('Error getting updates')
        return False

    if not request.status_code == 200:
        return False

    return request


if __name__ == "__main__":
    while True:
        try:
            check_updates()
            time.sleep(Settings.interval)
        except KeyboardInterrupt:
            print('Прервано пользователем..')
            break
