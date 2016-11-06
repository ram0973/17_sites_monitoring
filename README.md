# Решение задачи [№17](https://devman.org/challenges/17/) с сайта [devman.org](https://devman.org)

## Условие задачи:

Сайт недостаточно сделать и запустить. 
Нужно также обеспечить его работоспособность.

Добиться этого не всегда просто, здесь не обойтись без средств мониторинга. 
Как говорится, “кто предупреждён, тот вооружён".

Давай создадим утилиту для проверки состояния наших сайтов. 
На входе - текстовый файл с URL адресами для проверки. 
На выходе - статус каждого сайта по результатам следующих проверок:

сервер отвечает на запрос статусом HTTP 200;
доменное имя сайта проплачено как минимум на 1 месяц вперед.
С чего начать поиск решения:

[Статья про Хуиз на Википедии](https://ru.wikipedia.org/wiki/WHOIS)
[Статья про статусы ХТТП на Википедии](https://ru.wikipedia.org/wiki/Список_кодов_состояния_HTTP)

## Системные требования

```
Python 3.5.2+
win-unicode-console
python-whois
requests
python-dateutil
chardet
tqdm
```

## Установка

Windows

```    
git clone https://github.com/ram0973/17_sites_monitoring.git
cd 17_sites_monitoring
(Windows) pip install -r requirements.txt
(Linux) pip3 install -r requirements.txt
```
    
## Описание работы

```
Указываем путь к файлу со списком url, которые надо проверить.
Url должны быть **обязательно** со схемой, например: https://
Можно использовать домены второго уровня и ниже (третьего и т.д.).
Выводится список: url сайта, отвечает ли сайт кодом HTTP 200,
дата истечения оплаты домена, оплачен ли домен хотя бы на месяц.
При желании можно перехватить вывод в файл через > или >> 
(или дописать вывод в excel).
```

## Запуск

```
(Windows) python check_sites_health.py --i путь_до_файла_с_url_сайтов
(Linux) python3 check_sites_health.py --i путь_до_файла_с_url_сайтов
```
 
## Лицензия

[MIT](http://opensource.org/licenses/MIT)