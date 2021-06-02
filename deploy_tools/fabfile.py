from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
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
    sed(settings_path, 'ALLOWED_HOSTS =.+$', f'ALLOWED_HOSTS = ["{site_name}"]')
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

def _configure_nginx(source_folder):
    """заполнить и загрузить конфигурации Nginx и добавить сайт в автозагрузку"""
    nginx_template_file = f'{source_folder}/deploy_tools/nginx.template.conf'
    nginx_path = f'/etc/nginx'

    sed(nginx_template_file, 'SITENAME', env.host)
    sudo(f'cp -f {nginx_template_file} {nginx_path}/sites-available/{env.host}')
    sudo(f'ln -f -s {nginx_path}/sites-available/{env.host} {nginx_path}/sites-enabled/{env.host}')
    sudo(f'nginx -t')
    sudo('systemctl daemon-reload')
    sudo('systemctl reload nginx')

def _configure_gunicorn_as_service(source_folder):
    gunicorn_service_file = f'{source_folder}/deploy_tools/gunicorn-systemd.template.service'
    sed(gunicorn_service_file, 'SITENAME', env.host)
    sudo(f'cp -f {gunicorn_service_file} /etc/systemd/system/gunicorn-{env.host}.service')
    sudo('systemctl daemon-reload')
    sudo(f'rm /tmp/{env.host}.socket')
    sudo(f'systemctl enable gunicorn-{env.host}')
    sudo(f'systemctl stop gunicorn-{env.host}')
    sudo(f'systemctl start gunicorn-{env.host}')


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
    _configure_nginx(source_folder)
    _configure_gunicorn_as_service(source_folder)
