Обеcпечение работы нового сайта
================================
## Необходимые пакеты:
* nginx
* Python 3.7
* virtualenv + pip
* Git

В Ubuntu:

 sudo add-apt-repository ppa:deadsnakes/ppa

 sudo apt install nginx git python3.7 python3.7-venv

## Конфигурация виртального узла
* см. nginx.template.conf 
* заменить SITENAME на url

## Служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME на url

## Структура папок
- /home/username
  - sites
    - SITENAME
        - database
        - source
        - static
        - virtualenv
    