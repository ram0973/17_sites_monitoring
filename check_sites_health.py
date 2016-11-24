# -*- coding: utf-8 -*-
import argparse
import chardet
import requests
from tqdm import tqdm
from whois import whois
from datetime import datetime
from urllib.parse import urlparse
from dateutil.relativedelta import relativedelta

TIMEOUTS = (9, 9)


def load_urls4check(path):
    with open(path, mode='rb') as binary_file:
        file_encoding = chardet.detect(binary_file.read())['encoding']
    with open(path, mode='r', encoding=file_encoding) as urls:
        return [url.strip() for url in urls if url.strip()]


def is_server_respond_with_200(url):
    return requests.get(url, timeout=TIMEOUTS).status_code == 200


def get_domain_expiration_date(domain_name):
    who_is = whois('.'.join(domain_name.split('.')[-2:])).expiration_date
    return who_is[0] if isinstance(who_is, list) else who_is


def get_site_info(url):
    url_parts = urlparse(url)
    url_valid = url_parts.scheme and url_parts.netloc
    if not url_valid:
        return {'url': url, 'url_valid': False, 'status_200': None,
                'exp_date': None, 'is_paid': None}
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
    return {'url': url, 'url_valid': url_valid, 'status_200': status_200,
            'exp_date': exp_date, 'is_paid': is_paid}


def print_site_info(site):
    url = site['url']
    if not site['url_valid']:
        print('Maybe, wrong url: %s' % url)
        return
    status_200 = site['status200']
    exp_date = site['exp_date']
    is_paid = site['is_paid']
    status_200 = '-' if status_200 is None else ['No', 'Yes'][status_200]
    exp_date = '-' if exp_date is None else exp_date.strftime("%d.%m.%y")
    is_paid = '-' if is_paid is None else ['No', 'Yes'][is_paid]
    print('{:50}{:^10}{:^11}{:^9}'.format(url, status_200, exp_date, is_paid))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Checking sites status and their domain name payment')
    parser.add_argument('--file', '--f', help='Path to file with sites urls',
                        required=True)
    urls_file_path = parser.parse_args().file
    site_urls = load_urls4check(urls_file_path)
    print('\nChecking sites status and their domain name payment\n')
    print('Fetching data on sites by urls from file %s' % urls_file_path)
    sites_info = [get_site_info(site_url) for site_url in tqdm(site_urls)]
    print('\n{:50}{}{}{}'.format(
        'Site', ' Responds ', 'Paid until ', 'For month'))
    for site_info in sites_info:
        print_site_info(site_info)
