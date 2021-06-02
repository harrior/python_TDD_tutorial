from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

# Run as fab -i ..\..\authorized_keys  deploy:host=ubuntu@superlists-staging.harrior.ru

REPO_URL = "https://github.com/harrior/python_TDD_tutorial.git"


def _create_directory_structure_if_necessary(site_folder):
    """создать структуру каталога при неоходимости"""
    for subfolder in ('database', 'virtualenv', 'static', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    """получить самый свежий код проекта"""
    if exists(source_folder+'/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"cd {source_folder} && git reset --hard {current_commit}")


def _update_settings(source_folder, site_name):
    """обновить настройки"""
    settings_path = source_folder + '/superlistst/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'ALLOW_HOSTS =.+$', 'ALLOW_HOSTS =.+$', f'ALLOW_HOSTS = ["{site_name}"]')
    secret_key_file = source_folder + '/superlistst/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_vitrualenv(source_folder):
    """обновление виртуальной среды"""
    vitrualenv_folder = source_folder + '/../virtualenv'
    if not exists(vitrualenv_folder + '/bin/pip'):
        run(f'python3.7 -m venv {vitrualenv_folder}')
    run(f'{vitrualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    """обновить статаческие файлы"""
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    """обновить базу данных"""
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')


def deploy():
    """развернуть"""
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_vitrualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
