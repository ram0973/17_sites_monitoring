# -*- coding: utf-8 -*-
import argparse
import socket

import chardet
import requests
import sys
from tqdm import tqdm
from whois import whois
from datetime import datetime
from urllib.parse import urlparse
from dateutil.relativedelta import relativedelta

CONNECT_TIMEOUT = 9
READ_TIMEOUT = 9


def enable_unicode_in_windows():
    if sys.platform == 'win32':
        import win_unicode_console
        win_unicode_console.enable()


def handle_os_error(decorated):
    """ Декоратор исключений OSError, ошибка - выводим результат и выходим """
    def decorator(*args, **kwargs):
        try:
            return decorated(*args, **kwargs)
        except OSError as error:
            print('Ошибка: %s в файле: %s' % (error.strerror, error.filename))
            exit(1)
    return decorator


@handle_os_error
def load_urls4check(path: str) -> list:
    """
    Загружаем url сайтов из файла
    :param path: путь к файлу с url сайтов неизвестной кодировки
    :return список непустых url без табуляции, пробелов, переводов строк
    """
    with open(path, mode='rb') as binary_file:
        file_encoding = chardet.detect(binary_file.read())['encoding']
    with open(path, mode='r', encoding=file_encoding) as urls:
        return [url.strip(' \t\n\r') for url in urls if url.strip(' \t\n\r')]


def is_server_respond_with_200(url: str) -> bool:
    """ Проверяем, отвечает ли веб-сервер кодом статуса 200 """
    return requests.get(url, timeout=(
        CONNECT_TIMEOUT, READ_TIMEOUT)).status_code == 200


def get_domain_expiration_date(domain_name: str) -> datetime:
    """ Получаем дату окончания срока оплаты доменного имени """
    # информация от whois отдаётся только по домену 2 уровня
    domain_name = '.'.join(domain_name.split('.')[-2:])
    who_is = whois(domain_name).expiration_date
    return who_is[0] if isinstance(who_is, list) else who_is


def get_site_info(url: str) -> tuple:
    """
    Получаем информацию по сайту
    :param url: url сайта
    :return: кортеж (url, url_valid, status_200, exp_date, is_paid)
    is_paid = true, если домен оплачен хотя бы на месяц
    """
    url_parts = urlparse(url)
    url_valid = url_parts.scheme and url_parts.netloc
    # тут не стал добавлять http:// если его нет в url не знаю корректно ли это
    if not url_valid:
        return url, False, None, None, None
    try:
        status_200 = is_server_respond_with_200(url)
    except (requests.ConnectionError, requests.Timeout,
            requests.TooManyRedirects):
        status_200 = None

    exp_date = get_domain_expiration_date(urlparse(url).netloc)
    if exp_date:
        is_paid = relativedelta(exp_date, datetime.today()).months > 0
    else:
        exp_date = None
        is_paid = None

    # не знаю, праильно ли тут использовать кортеж
    return url, url_valid, status_200, exp_date, is_paid


def print_site_info(site: tuple):
    """ Печатаем информацию по сайту """
    url, url_valid, status_200, exp_date, is_paid = site
    if not url_valid:
        print('Возможно, неверный url: %s' % url)
        return
    status_200 = '-' if status_200 is None else ['Нет', 'Да'][status_200]
    exp_date = '-' if exp_date is None else exp_date.strftime("%d.%m.%y")
    is_paid = '-' if is_paid is None else ['Нет', 'Да'][is_paid]
    print('{:50}{:^10}{:^11}{:^9}'.format(url, status_200, exp_date, is_paid))


def get_args_parser():
    parser = argparse.ArgumentParser(
        description='Проверка статуса сайтов и оплаты доменного имени')
    parser.add_argument('--file', '--f', help='Путь к файлу с url сайтов',
                        # type=argparse.FileType(mode='r',),
                        # required=True
                        )
    return parser


def main():
    enable_unicode_in_windows()
    args_parser = get_args_parser()
    urls_file_path = args_parser.parse_args().file
    if not urls_file_path:
        print('Ошибка: вы не задали путь к файлу с url сайтов')
        args_parser.print_usage()
        exit(1)

    site_urls = load_urls4check(urls_file_path)

    print('\nПроверка статуса сайтов и оплаты доменного имени\n')
    print('Получаем данные по сайтам из файла %s' % urls_file_path)
    sites_info = [get_site_info(site_url) for site_url in tqdm(site_urls)]

    print('\n{:50}{}{}{}'.format(
        'Сайт', ' Отвечает ', 'Оплачен до, ', 'за месяц'))
    for site_info in sites_info:
        print_site_info(site_info)


if __name__ == '__main__':
    main()
