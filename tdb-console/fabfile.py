# -*- coding: utf-8 -*-
import os
from fabric.api import run, env, cd, prefix, sudo, settings, task
from fabric.contrib.project import rsync_project


def update_repo(file_path):
    run('mkdir -p {}'.format(file_path))
    rsync_project(local_dir='build/temp/', remote_dir=file_path, exclude=('.git', 'fabfile.py', 'venv'))


def install_docker():
    with settings(warn_only=True):
        if run('service docker start').failed:
            run('sudo yum install docker -y')

        run('service docker start')
        run('chkconfig docker on')


def run_docker_container(docker_ssh_port, nginx_listen_port, container_name, docker_image):
    run('docker logout')
    # 此处不要加 -u -p 防止记录
    with settings(prompts={'Username: ': 'lxzle', 'Password: ': 'lxzle123'}):
        run('docker login')
    with settings(warn_only=True):
        run('docker container run --restart=always -p {}:22 -p {}:{} --name={} -d -it {}'.format(
            docker_ssh_port, nginx_listen_port, nginx_listen_port, container_name, docker_image))
    run('docker logout')
    # run('docker exec -it test-api /bin/bash')
    # run('exit')

    # docker stop test-prj && docker rm test-prj && docker image rm $(docker image ls) 删除所有容器及镜像
    # docker commit -m "install gcc" test-api centos-software 提交镜像
    # docker tag centos-software lxzle/project:centos.software.v1_0_2 打tag
    # docker push lxzle/project:centos.software.v1_0_2 推送
    # docker update --restart=always test-prj 如果test-prj工程加少参数--restart 可以直接用update更新

    # 在已经运行的docker中添加端口如下：
    # 1. service docker stop
    # 2. cd /var/lib/docker/containers/[name]/hostconfig.json 添加所需的端口 PortBindings 中
    # 3. cd /var/lib/docker/containers/[name]/config.v2.json 添加所需的端口 ExposedPorts 中
    # 4. service docker start


def nginx_config(nginx_listen_port, domain_name, project, project_port):
    nginx_conf = \
        '''\'server {{
          listen {};
          server_name {};
          location / {{
              proxy_pass http://127.0.0.1:{};
              proxy_set_header    Host    $http_host;
          }}
        }}\''''.format(nginx_listen_port, domain_name, project_port)

    run('echo -e {} > /etc/nginx/conf.d/{}.conf'.format(nginx_conf, project))
    run('nginx -t')
    run('nginx -s reload')


@task
def deploy_test():
    env.host_string = 'root@47.75.207.244'
    mode = 'STAGING'
    port = 9003
    processes = 1
    project = 'lebo-console'

    # docker 所需参数
    docker_ssh_port = 422
    nginx_listen_port = 80
    docker_image = 'lxzle/project:centos.software.v1_0_5'
    container_name = 'test-prj'
    domain_name = 'console.lebo.test.eos-club.in'

    # 是否使能docker
    deploy_by_docker = False
    install_dir = '/root/{}'.format(project)

    print ('building')
    os.system('cd build && npm install && npm install grunt && grunt build')

    if deploy_by_docker:
        install_docker()
        run_docker_container(docker_ssh_port, nginx_listen_port, container_name, docker_image)
        env.port = docker_ssh_port
    nginx_config(nginx_listen_port, domain_name, project, port)

    update_repo(install_dir)
    with cd(install_dir):
        with settings(warn_only=True):
            v_env_failed = run('ls venv').failed

        # 安装虚拟环境
        if v_env_failed:
            with settings(warn_only=True):
                install_v_env_failed = run('virtualenv venv').failed

            if install_v_env_failed:
                run('pip install virtualenv')
                run('virtualenv venv')

        with prefix('. venv/bin/activate'):
            run('pip uninstall -y Cython')
            run('pip install -r requirements/production.txt')
            # run('python setup.py build_ext --inplace')

        with settings(warn_only=True):
            # 新建logs文件夹
            run('mkdir -p {}/logs'.format(install_dir))
            # 新建tmp文件夹
            run('mkdir -p {}/tmp'.format(install_dir))
            update_failed = run(
                'export INSTALL_DIR={} MODE={} apiPort={} processes={} &&'
                'venv/bin/supervisorctl -c '
                'supervisord.conf update'.format(install_dir, mode.upper(), port, processes)).failed

            if update_failed:
                run('export INSTALL_DIR={} MODE={} apiPort={} processes={} &&'
                    'venv/bin/supervisord -c '
                    'supervisord.conf'.format(install_dir, mode.upper(), port, processes))
            else:
                run('export INSTALL_DIR={} MODE={} apiPort={} processes={} &&'
                    'venv/bin/supervisorctl -c '
                    'supervisord.conf restart all'.format(install_dir, mode.upper(), port, processes))
        # run('rm -rf app/views  .git')
        run('find app/ -name "*.py*" ! -name "__init__.py" | xargs -i rm -f {}')
        run('find app/ -name "*.c" | xargs -i rm -f {}')
        run('rm -rf build')


@task
def deploy_online():
    env.host_string = 'root@47.244.41.115'
    env.password = 'tymmgg1+'
    mode = 'PRODUCTION'
    port = 9003
    processes = 3
    project = 'lebo-console'

    # docker 所需参数
    docker_ssh_port = 422
    nginx_listen_port = 80
    docker_image = 'lxzle/project:centos.software.v1_0_5'
    container_name = 'test-prj'
    domain_name = 'console.lebo2019plus.com'

    # 是否使能docker
    deploy_by_docker = False
    install_dir = '/root/{}'.format(project)

    print ('building')
    os.system('cd build && npm install && npm install grunt && grunt build')

    if deploy_by_docker:
        install_docker()
        run_docker_container(docker_ssh_port, nginx_listen_port, container_name, docker_image)
        env.port = docker_ssh_port
    nginx_config(nginx_listen_port, domain_name, project, port)

    update_repo(install_dir)
    with cd(install_dir):
        with settings(warn_only=True):
            v_env_failed = run('ls venv').failed

        # 安装虚拟环境
        if v_env_failed:
            with settings(warn_only=True):
                install_v_env_failed = run('virtualenv venv').failed

            if install_v_env_failed:
                run('pip install virtualenv')
                run('virtualenv venv')

        with prefix('. venv/bin/activate'):
            run('pip uninstall -y Cython')
            run('pip install -r requirements/production.txt')
            run('python setup.py build_ext --inplace')

        with settings(warn_only=True):
            # 新建logs文件夹
            run('mkdir -p {}/logs'.format(install_dir))
            # 新建tmp文件夹
            run('mkdir -p {}/tmp'.format(install_dir))
            update_failed = run(
                'export INSTALL_DIR={} MODE={} apiPort={} processes={} &&'
                'venv/bin/supervisorctl -c '
                'supervisord.conf update'.format(install_dir, mode.upper(), port, processes)).failed

            if update_failed:
                run('export INSTALL_DIR={} MODE={} apiPort={} processes={} &&'
                    'venv/bin/supervisord -c '
                    'supervisord.conf'.format(install_dir, mode.upper(), port, processes))
            else:
                run('export INSTALL_DIR={} MODE={} apiPort={} processes={} &&'
                    'venv/bin/supervisorctl -c '
                    'supervisord.conf restart all'.format(install_dir, mode.upper(), port, processes))
        # run('rm -rf app/views  .git')
        run('find app/ -name "*.py*" ! -name "__init__.py" | xargs -i rm -f {}')
        run('find app/ -name "*.c" | xargs -i rm -f {}')
        run('rm -rf build')