# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager
from fabric.api import cd, env, prefix, run, task, shell_env, sudo
from fabric.context_managers import hide, settings
from fabric.contrib.project import rsync_project


def update_repo(file_path, project):
    run('mkdir -p {}'.format(file_path))
    rsync_project(remote_dir=file_path + '/' + project, local_dir=os.getcwd() + '/',
                  exclude=('.git', 'fabfile.py', 'venv'))
    # 新建logs文件夹
    run('mkdir -p {}/logs'.format(file_path))
    # 新建tmp文件夹
    run('sudo mkdir -p /tmp/{}'.format(file_path[2:]))
    # 新建nginx log 文件夹
    run('sudo mkdir -p /var/log/nginx/{}'.format(file_path[2:]))


def build(project, mode, file_path):
    with cd('{}/{}'.format(file_path, project)):
        # 检查虚拟环境
        with settings(warn_only=True):
            v_env_failed = run('ls venv').failed

        # 安装虚拟环境
        if v_env_failed:
            with settings(warn_only=True):
                install_v_env_failed = run('virtualenv -p python3.6 venv').failed

            if install_v_env_failed:
                run('sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm')
                run('sudo yum makecache')
                run('sudo yum -y install python36u')
                run('sudo yum -y install python36u-pip')
                run('sudo yum install -y mariadb-devel mysql-devel python36u-devel python-setuptools')
                run('sudo pip install virtualenv')
                run('virtualenv -p python3.6  venv')
                run(
                    'sudo rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm')
                run('sudo yum install -y nginx')

        # 检查 数据库版本管理
        with settings(warn_only=True):
            ls_migrations_failed = run('ls migrations').failed

        # 安装依赖包
        with prefix('. venv/bin/activate'):
            run('pip3 uninstall -y Cython')
            run('pip3 install -r requirements/production.txt')

            run('python setup.py build_ext --inplace')
            run('find app/json_rpc/ -name "*.py*" ! -name "__init__.py" ! -name "engine.py" | xargs -i rm -f {}')
            run('find -name "*.c" | xargs -i rm -f {}')
            run('rm -rf build')

            # 更新数据库版本
            with shell_env(MODE=mode):
                run('python manage.py db upgrade')
                run('python manage.py update_setting')
                run('python manage.py db_initialize')


def restart_online_service(project, mode, processes, file_path):
    install_dir = '{}/{}'.format(file_path, project)
    with cd(install_dir):
        # 更新 检查 supervisord 环境
        with settings(warn_only=True):
            update_failed = run(
                'export INSTALL_DIR={} MODE={} processes={} project={} &&'
                'sudo -E supervisorctl -c '
                'deploy/supervisord.conf update'.format(install_dir, mode, processes, project)).failed

        if update_failed:
            run('export INSTALL_DIR={} MODE={} processes={} project={} &&'
                'sudo -E supervisord -c '
                'deploy/supervisord.conf'.format(install_dir, mode, processes, project))
        else:
            run('export INSTALL_DIR={} MODE={} processes={} project={} &&'
                'sudo -E supervisorctl -c '
                'deploy/supervisord.conf restart all'.format(install_dir, mode, processes, project))


def restart_test_service(project, mode, processes, file_path):
    install_dir = '{}/{}'.format(file_path, project)
    with cd(install_dir):
        # 更新 检查 supervisord 环境
        with settings(warn_only=True):
            update_failed = run(
                'export INSTALL_DIR={} MODE={} processes={} project={} &&'
                'sudo -E supervisorctl -c '
                'deploy/supervisord.conf update'.format(install_dir, mode, processes, project)).failed

        if update_failed:
            run('export INSTALL_DIR={} MODE={} processes={} project={} &&'
                'sudo -E supervisord -c '
                'deploy/supervisord.conf'.format(install_dir, mode, processes, project))

        else:
            run('export INSTALL_DIR={} MODE={} processes={} project={} &&'
                'sudo -E supervisorctl -c '
                'deploy/supervisord.conf restart all'.format(install_dir, mode, processes, project))


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


def nginx_config(domain_name, project, mode):
    nginx_conf = \
        '''\'
        upstream {project}-{mode} {{ server unix:/tmp/{project}/{mode}/api.sock;}}
        server {{
          listen {};
          server_name {domain_name};
          
          access_log  /var/log/nginx/{project}/{mode}/access.log;
          error_log   /var/log/nginx/{project}/{mode}/error.log;
          charset     utf-8;
          
          #Max upload size
          client_max_body_size 200M;   # adjust to taste

          location / {{
              proxy_pass http://{project}-{mode};
              proxy_set_header    Host    $http_host;
          }}
          
        }}\''''.format(80, domain_name=domain_name, project=project, mode=mode)

    run('echo -e {} > /etc/nginx/conf.d/{}-{}.conf'.format(nginx_conf, project, mode))
    run('nginx -t')
    run('nginx -s reload')


@task
def deploy_test():
    env.host_string = 'root@47.75.207.244'
    env.use_ssh_config = True
    mode = 'staging'
    project = 'lebo-api'
    processes = 1

    # docker 所需参数
    docker_ssh_port = 422
    nginx_listen_port = 80
    docker_image = 'lxzle/project:centos.software.v1_0_5'
    container_name = 'test-prj'  # 测试全部放在这个容器中
    domain_name = 'api.lebo.test.eos-club.in'

    # 是否使能docker
    deploy_by_docker = False

    file_path = '~/{}/{}'.format(project, mode)

    if deploy_by_docker:
        install_docker()
        run_docker_container(docker_ssh_port, nginx_listen_port, container_name, docker_image)
        env.port = docker_ssh_port

    update_repo(file_path, project)
    nginx_config(domain_name, project, mode)
    build(project, mode, file_path)
    restart_test_service(project, mode, processes, file_path)


@task
def deploy_online():
    env.host_string = 'root@47.244.41.115'
    env.password = 'tymmgg1+'
    # env.use_ssh_config = True
    mode = 'production'
    project = 'lebo-api'
    processes = 8

    # docker 所需参数
    docker_ssh_port = 422
    nginx_listen_port = 80
    docker_image = 'lxzle/project:centos.software.v1_0_5'
    container_name = 'test-prj'  # 测试全部放在这个容器中
    domain_name = 'api.lebo2019plus.com'

    # 是否使能docker
    deploy_by_docker = False

    file_path = '~/{}/{}'.format(project, mode)

    if deploy_by_docker:
        install_docker()
        run_docker_container(docker_ssh_port, nginx_listen_port, container_name, docker_image)
        env.port = docker_ssh_port

    update_repo(file_path, project)
    build(project, mode, file_path)
    restart_online_service(project, mode, processes, file_path)
    nginx_config(domain_name, project, mode)
