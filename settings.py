#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class Settings:

    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Интервал проверки наличия новых сообщений (обновлений) на сервере в секундах
    interval = 3

    # Адрес HTTP Bot API
    urlBot = 'https://api.telegram.org/bot'

    urlFile = 'https://api.telegram.org/file/bot'

    # ID пользователя. Комманды от других пользователей выполняться не будут
    adminId = 0

    # Ключ авторизации для Вашего бота
    token = ''  # Ключ авторизации для Вашего бота

    # ID последнего полученного обновления
    offset = 0