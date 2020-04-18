# MeowMeowGo

Реализация простой поисковой системы. Итерация 1 - реализация поискового робота

## To do

Реализовать веб-интерфейс

## Установка и запуск

Установка MeowMeowGo
    
```
$ git clone https://github.com/pash4paul/meow-meow-go.git
$ cd meow-meow-go
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

Установка и настройка базы данных

```
$ sudo apt install postgresql-12
$ sudo -u postgres psql < db_init.sql
```

!!! Ознакомиться с настройками в config.py

Запуск паука

```
$ python3 start_crawler.py
```

## Built With

* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Beautiful Soup is a Python library for pulling data out of HTML and XML files
* [bloom-filter](https://pypi.org/project/bloom-filter/) - A pure python bloom filter
* [PostgreSQL 12](https://www.postgresql.org/) - PostgreSQL: The World's Most Advanced Open Source Relational Database
* [psycopg2](https://www.psycopg.org/) - Psycopg is the most popular PostgreSQL adapter for the Python programming language
* [requests](https://requests.readthedocs.io/en/master/) - Requests: HTTP for Humans

## Автор

* **Pavel Fomin** - [pash4paul](https://github.com/pash4paul)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
